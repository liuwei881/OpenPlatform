#coding=utf-8

from celery import Celery, task
import json
import nginx
import logging
import os
import datetime
try:
    from salt_api import api_login, get_result
except Exception as e:
    from .salt_api import api_login, get_result


celery = Celery("tasks", broker="amqp://")
celery.conf.CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'amqp')
celery.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_RESULT_SERIALIZER='json',
    CELERY_ROUTES = {
            'tasks.nginx_issue': {'queue':'issue'},
            'tasks.issue_del': {'queue':'issue'},
    })


@celery.task(name='tasks.nginx_issue')
def nginx_issue(domainname, port, healthexam):
    """nginx 发布 consul reload, add upstream, add vhost reload cosnul-template"""
    fmt = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
    logging.basicConfig(level=logging.INFO,
                        format=fmt,
                        datefmt='%Y-%m-%d_%H:%M:%S',
                        filename='./nginx.log',
                        filemode='aw')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter(fmt)
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)
    # create web.json
    get_result('cmd.run',
               'cp /data/salt/web.json /data/salt/json_back/web.json.{0}'.format(
                datetime.datetime.now().strftime('%Y-%m-%d_%H:%M')), tgt="10.96.5.95")
    res = {}
    res["id"] = domainname
    res["name"] = domainname
    res["tags"] = []
    res["tags"].append(domainname)
    res["port"] = int(port)
    res["checks"] = []
    res["checks"].append({})
    res["checks"][0]["name"] = "_".join(["nginx", domainname])
    res["checks"][0]["http"] = "http://localhost:{0}{1}".format(port, healthexam)
    res["checks"][0]["interval"] = "5s"
    res["checks"][0]["timeout"] = "2s"
    with open("/data/salt/web.json", "r") as f:
        a = dict(json.loads(f.read()))
        a["services"].append(res)
    with open("/data/salt/web.json", "w") as f:
        f.write(json.dumps(a, indent=4))
    logging.info('create web.json finish')
    # salt cp file to consul client and reload consul use salt-api
    get_result('cp.get_file', ['salt://web.json','/etc/consul.d/agent/web.json'],
               tgt="rancher_group", expr_form="nodegroup")
    get_result('cmd.run', '/usr/local/bin/consul reload',
               tgt="rancher_group", expr_form="nodegroup")
    logging.info('cp web.json to consul client and reload consul finish')
    with open('/data/salt/nginx_temp/upstream/{0}.conf'.format(domainname), 'w') as f:
        pass
    # create server
    c = nginx.Conf()
    s = nginx.Server()
    s.add(
        nginx.Key('listen', '80'),
        nginx.Key('server_name', '{0}.openkf.cn'.format(domainname)),
        nginx.Key('access_log', '/var/log/nginx/{0}.openkf.cn.log  main'.format(domainname)),
        nginx.Location('/',
            nginx.Key('proxy_pass', 'http://{0}'.format(domainname)),
            nginx.Key('proxy_set_header', 'Host $host'),
            nginx.Key('proxy_set_header', 'X-Real-IP $remote_addr'),
            nginx.Key('proxy_set_header', 'X-Forwarded-For $proxy_add_x_forwarded_for')
            )
        )
    c.add(s)
    nginx.dumpf(c, '/data/salt/nginx_temp/vhosts/{0}.openkf.cn.conf'.format(domainname))
    logging.info("create {0}.openkf.cn.conf finish".format(domainname))

    # create consul template
    c = nginx.Conf()
    u = nginx.Upstream('{0}'.format(domainname),
        nginx.Key('ip_hash', ''),
        nginx.Key('{{range service "%s"}}' % domainname, ''),
        nginx.Key('server', '{{.Address}}:{{.Port}} fail_timeout=0'),
        nginx.Key('{{else}}', ''),
        nginx.Key('server', '10.100.20.31:80'),
        nginx.Key('{{end}}', ''),
        nginx.Key('keepalive', '64')
        )
    c.add(u)
    nginx.dumpf(c, '/data/salt/nginx_temp/consul_nginx_temp/{0}.ctmpl'.format(domainname))
    with open('/data/salt/nginx_temp/consul_nginx_temp/{0}.ctmpl'.format(domainname), 'r') as f:
        fs = f.readlines()
    fst = []
    for i in fs:
        if i.endswith('} ;\n'):
            i = i.replace('} ;\n', '} \n')
        fst.append(i)
    with open('/data/salt/nginx_temp/consul_nginx_temp/{0}.ctmpl'.format(domainname), 'w') as f:
        f.write(''.join(fst))
    logging.info('create {0}.ctmpl finish'.format(domainname))

    # update consul_temp.conf
    get_result('cmd.run',
               'cp /data/salt/nginx_temp/consul_nginx_temp/consul_temp.conf /data/salt/nginx_temp/consul_nginx_temp/consul_temp.conf.{0}'.format(
                   datetime.datetime.now().strftime('%Y-%m-%d_%H:%M')), tgt="10.96.5.95")
    with open("/data/salt/nginx_temp/consul_nginx_temp/consul_temp.conf", 'r') as f:
        fs = f.readlines()
    a = 'template {\n', ' source = "/data/nginx_consul_template/{0}.ctmpl"\n'.format(
        domainname), ' destination = "/usr/local/nginx/upstream/{0}.conf"\n'.format(
        domainname), ' command = "systemctl reload nginx"\n', '}\n'
    for i in a:
        fs.append(i)
    with open("/data/salt/nginx_temp/consul_nginx_temp/consul_temp.conf", 'w') as f:
        f.write(''.join(fs))
    logging.info('update consul_temp.conf finish')

    # cp upstream vhosts ctmpl consul_temp to nginx server and reload consul-template use salt-api
    get_result('cp.get_file', ['salt://nginx_temp/consul_nginx_temp/{0}.ctmpl'.format(domainname),
                               '/data/nginx_consul_template/{0}.ctmpl'.format(domainname)], tgt="10.96.5.95")
    get_result('cp.get_file', ['salt://nginx_temp/vhosts/{0}.openkf.cn.conf'.format(domainname),
                               '/usr/local/nginx/vhosts/{0}.openkf.cn.conf'.format(domainname)], tgt="10.96.5.95")
    get_result('cp.get_file', ['salt://nginx_temp/upstream/{0}.conf'.format(domainname),
                               '/usr/local/nginx/upstream/{0}.conf'.format(domainname)], tgt="10.96.5.95")
    get_result('cp.get_file', ['salt://nginx_temp/consul_nginx_temp/consul_temp.conf',
                               '/data/consul_template/consul_temp.conf'], tgt="10.96.5.95")
    get_result('cmd.run', 'kill -HUP `cat /var/run/consul-template.pid`', tgt="10.96.5.95")
    logging.info('reload nginx and consul-template finish')
    return "reload nginx and consul-template finish domainname {0}".format(domainname)


@celery.task(name='tasks.issue_del')
def issue_del(domainname):
    """nginx 项目删除 清除nginx配置和consul-template配置"""
    fmt = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
    logging.basicConfig(level=logging.INFO,
                        format=fmt,
                        datefmt='%Y-%m-%d_%H:%M:%S',
                        filename='./nginx.log',
                        filemode='aw')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)

    formatter = logging.Formatter(fmt)
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)

    # del web.json
    # back web.json
    get_result('cmd.run', 'cp /data/salt/web.json /data/salt/json_back/web.json.{0}'.format(
        datetime.datetime.now().strftime('%Y-%m-%d_%H:%M')), tgt="10.96.5.95")
    with open("/data/salt/web.json", "r") as f:
        a = json.loads(f.read())
        a = dict(a)
        [a['services'].remove(i) for i in a['services'] if domainname == i['name']]

    with open("/data/salt/web.json", "w") as f:
        f.write(json.dumps(a, indent=4))
    logging.info('del web.json finish')

    # salt cp file to consul client and reload consul
    get_result('cp.get_file', ['salt://web.json', '/etc/consul.d/agent/web.json'],
               tgt="rancher_group", expr_form="nodegroup")
    get_result('cmd.run', '/usr/local/bin/consul reload',
               tgt="rancher_group", expr_form="nodegroup")

    logging.info('cp web.json to consul client and reload consul finish')

    # del consul_temp.conf
    get_result('cmd.run',
               'cp /data/salt/nginx_temp/consul_nginx_temp/consul_temp.conf /data/salt/nginx_temp/consul_nginx_temp/consul_temp.conf.{0}'.format(
                   datetime.datetime.now().strftime('%Y-%m-%d_%H:%M')), tgt="10.96.5.95")
    with open("/data/salt/nginx_temp/consul_nginx_temp/consul_temp.conf", 'r') as fp:
        fp = fp.readlines()
    for i in fp:
        if domainname in i and i.startswith(' source'):
            fp = fp[0:fp.index(i) - 1] + fp[fp.index(i) + 4:]
    with open("/data/salt/nginx_temp/consul_nginx_temp/consul_temp.conf", 'w') as f:
        f.write(''.join(fp))
    logging.info('update consul_temp.conf finish')
    # cp upstream vhosts ctmpl consul_temp to nginx server and reload consul-template
    get_result('cmd.run', 'rm /usr/local/nginx/upstream/{0}.conf -rf'.format(domainname), tgt="10.96.5.95")
    get_result('cmd.run', 'rm /usr/local/nginx/vhosts/{0}.openkf.cn.conf -rf'.format(domainname), tgt="10.96.5.95")
    get_result('cmd.run', 'rm /data/nginx_consul_template/{0}.ctmpl -rf'.format(domainname), tgt="10.96.5.95")
    get_result('cp.get_file', ['salt://nginx_temp/consul_nginx_temp/consul_temp.conf',
                               '/data/consul_template/consul_temp.conf'], tgt="10.96.5.95")
    get_result('cmd.run', 'kill -HUP `cat /var/run/consul-template.pid`', tgt="10.96.5.95")
    logging.info('reload nginx and consul-template finish')
    return "del nginx and consul-template finish domainname {0}".format(domainname)