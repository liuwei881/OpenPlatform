#coding=utf-8

from celery import Celery, task
import os
import datetime
import dns.tsigkeyring
import dns.update
import dns.query
try:
    from salt_api import api_login, get_result
except Exception as e:
    from .salt_api import api_login, get_result


# celery = Celery("tasks", broker="amqp://")
celery = Celery("tasks", broker="amqp://admin:open@2018@rabbitmq.sysgroup.open.com.cn:5672//")
celery.conf.CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'amqp')


celery.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_RESULT_SERIALIZER='json',
    CELERY_ROUTES={
        'tasks.nginx_release': {'queue': 'release'},
        'tasks.release_del': {'queue': 'release'},
        'tasks.ready_release': {'queue': 'release'},
        'tasks.tcp_release': {'queue': 'release'},
        'tasks.tcp_release_del': {'queue': 'release'},
        'tasks.ready_release_del': {'queue': 'release'},
        'tasks.dns_resolution': {'queue': 'release'},
    })


@celery.task(name='tasks.nginx_release')
def nginx_release(domainname, port, healthexam):
    """nginx 发布 consul reload, add upstream, add vhost reload cosnul-template"""
    get_result('cmd.run',
               'cp /data/salt/web.json /data/salt/json_back/web.json.{0}'.format(
                datetime.datetime.now().strftime('%Y-%m-%d_%H:%M')), tgt="vmlin0520.open.com.cn")
    get_result('cmd.run',
               '/usr/bin/python2.7 /data/salt/consul_nginx.py {0} {1} {2}'.format(
                   domainname, port, healthexam), tgt='vmlin0520.open.com.cn')
    return "Release {0} is finish".format(domainname)


@celery.task(name='tasks.release_del')
def release_del(domainname):
    """nginx 项目删除 清除nginx配置和consul-template配置"""
    get_result('cmd.run',
               '/usr/bin/python2.7 /data/salt/consul_nginx_del.py {0}'.format(domainname), tgt='vmlin0520.open.com.cn')
    return "del {0} is finish".format(domainname)


@celery.task(name='tasks.ready_release')
def ready_release(name, port, domainname, healthexam):
    """预生产发布nginx及consul"""
    get_result('cmd.run',
               'cp /data/salt/web_pre.json /data/salt/json_back/web_pre.json.{0}'.format(
                   datetime.datetime.now().strftime('%Y-%m-%d_%H:%M')), tgt="vmlin0520.open.com.cn")
    get_result('cmd.run',
               '/usr/bin/python2.7 /data/salt/consul_nginx_pre.py {0} {1} {2} {3}'.format(
                   name, port, domainname, healthexam), tgt='vmlin0520.open.com.cn')
    return "Release {0} is finish".format(domainname)


@celery.task(name='tasks.ready_release_del')
def ready_release_del(domainname):
    """删除预生产nginx及consul-template配置"""
    get_result('cmd.run',
               '/usr/bin/python2.7 /data/salt/consul_nginx_del_pre.py {0}'.format(domainname), tgt='vmlin0520.open.com.cn')
    return "Release {0} is finish".format(domainname)


@celery.task(name='tasks.tcp_release')
def nginx_tcp_release(domainname, port):
    """nginx 4层发布 consul reload, add upstream, add vhost reload cosnul-template"""
    get_result('cmd.run',
               'cp /data/salt/web_tcp.json /data/salt/json_back/web_tcp.json.{0}'.format(
                datetime.datetime.now().strftime('%Y-%m-%d_%H:%M')), tgt="vmlin0520.open.com.cn")
    get_result('cmd.run',
               '/usr/bin/python2.7 /data/salt/consul_nginx_tcp.py {0} {1}'.format(
                   domainname, port), tgt='vmlin0520.open.com.cn')
    return "Release {0} is finish".format(domainname)


@celery.task(name='tasks.tcp_release_del')
def release_del(domainname):
    """nginx 项目删除 清除nginx配置和consul-template配置"""
    get_result('cmd.run',
               '/usr/bin/python2.7 /data/salt/consul_nginx_tcp_del.py {0}'.format(domainname),
               tgt='vmlin0520.open.com.cn')
    return "del {0} is finish".format(domainname)


@celery.task(name='tasks.dns_resolution')
def dns_resolution(action, name, ttl, _type, value):
    """发布openkf.cn直接解析"""
    keyring = dns.tsigkeyring.from_text({'other-key': 'WWFjaI4lkvXNkRAIExbFYA=='})
    up = dns.update.Update('openkf.cn', keyring=keyring)
    server = '10.100.14.219'
    server2 = '10.100.132.16'
    if action == 'add':
        up.add(name, ttl, _type, value)
        dns.query.tcp(up, server)
        dns.query.tcp(up, server2)
    elif action == 'delete':
        up.delete(name, _type)
        dns.query.tcp(up, server)
        dns.query.tcp(up, server2)
        return 'delete {0} to {1} is ok'.format(name, value)
    return 'resolution {0} to {1} is ok'.format(name, value)