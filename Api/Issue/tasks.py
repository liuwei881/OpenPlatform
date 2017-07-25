#coding=utf-8

from celery import Celery, task
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
    get_result('cmd.run',
               'cp /data/salt/web.json /data/salt/json_back/web.json.{0}'.format(
                datetime.datetime.now().strftime('%Y-%m-%d_%H:%M')), tgt="vmlin0520.open.com.cn")
    get_result('cmd.run',
               '/usr/bin/python2.7 /data/salt/consul_nginx.py {0} {1} {2}'.format(
                   domainname, port, healthexam), tgt='vmlin0520.open.com.cn')
    return "issue {0} is finish".format(domainname)


@celery.task(name='tasks.issue_del')
def issue_del(domainname):
    """nginx 项目删除 清除nginx配置和consul-template配置"""
    get_result('cmd.run',
               '/usr/bin/python2.7 /data/salt/consul_nginx_del.py {0}'.format(domainname), tgt='vmlin0520.open.com.cn')
    return "del {0} is finish".format(domainname)