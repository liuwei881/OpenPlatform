#coding=utf-8

from celery import Celery, task
import os
import dns.tsigkeyring
import dns.update
import dns.query


celery = Celery("tasks", broker="amqp://")
celery.conf.CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'amqp')
celery.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_RESULT_SERIALIZER='json',
    CELERY_ROUTES = {
        'tasks.resolution': {'queue': 'resolution'},
        'tasks.resolution_edit': {'queue': 'resolution'},
        'tasks.resolution_del': {'queue': 'resolution'},
    })


@celery.task(name='tasks.resolution')
def resolution(zone, name, ttl, _type, value):
    """添加DNS解析"""
    # bind9 server
    server = '10.96.5.96'
    if zone == "open.com.cn" and _type == 'A':
        if "10.100" in value or "10.96" in value:
            keyring = dns.tsigkeyring.from_text({'other-key': 'WWFjaI4lkvXNkRAIExbFYA=='})
            up = dns.update.Update(zone, keyring=keyring)
            up.add(name, ttl, _type, value)
            dns.query.tcp(up, server)
            # for win AD
            server2 = "10.96.5.58"
            up = dns.update.Update(zone)
            up.add(name, ttl, _type, value)
            dns.query.tcp(up, server2)
        else:
            keyring = dns.tsigkeyring.from_text({'other-key': 'WWFjaI4lkvXNkRAIExbFYA=='})
            up = dns.update.Update(zone, keyring=keyring)
            up.add(name, ttl, _type, value)
            dns.query.tcp(up, server)
            keyring2 = dns.tsigkeyring.from_text({'otheri-key': 'AAFjaI4lkvXNkRAIExbFYA=='})
            up2 = dns.update.Update(zone, keyring=keyring2)
            up2.add(name, ttl, _type, value)
            dns.query.tcp(up2, server)
    else:
        keyring = dns.tsigkeyring.from_text({'other-key': 'WWFjaI4lkvXNkRAIExbFYA=='})
        up = dns.update.Update(zone, keyring=keyring)
        up.add(name, ttl, _type, value)
        dns.query.tcp(up, server)
        keyring2 = dns.tsigkeyring.from_text({'otheri-key': 'AAFjaI4lkvXNkRAIExbFYA=='})
        up2 = dns.update.Update(zone, keyring=keyring2)
        up2.add(name, ttl, _type, value)
        dns.query.tcp(up2, server)
    return "DNS update {0} finish".format(name)


@celery.task(name='tasks.resolution_edit')
def resolution_edit(zone, name, ttl, _type, value):
    """修改DNS解析"""
    server = "10.96.5.96"
    if zone == "open.com.cn" and _type == 'A':
        if "10.100" in value or "10.96" in value:
            keyring = dns.tsigkeyring.from_text({'other-key': 'WWFjaI4lkvXNkRAIExbFYA=='})
            up = dns.update.Update(zone, keyring=keyring)
            up.delete(name, _type)
            up.add(name, ttl, _type, value)
            dns.query.tcp(up, server)
            # for win AD
            server = "10.96.5.58"
            up = dns.update.Update(zone)
            up.delete(name, _type)
            up.add(name, ttl, _type, value)
            dns.query.tcp(up, server)
        else:
            keyring = dns.tsigkeyring.from_text({'other-key': 'WWFjaI4lkvXNkRAIExbFYA=='})
            up = dns.update.Update(zone, keyring=keyring)
            up.delete(name, _type)
            up.add(name, ttl, _type, value)
            dns.query.tcp(up, server)
            keyring2 = dns.tsigkeyring.from_text({'otheri-key': 'AAFjaI4lkvXNkRAIExbFYA=='})
            up2 = dns.update.Update(zone, keyring=keyring2)
            up2.delete(name, _type)
            up2.add(name, ttl, _type, value)
            dns.query.tcp(up2, server)
    else:
        keyring = dns.tsigkeyring.from_text({'other-key': 'WWFjaI4lkvXNkRAIExbFYA=='})
        up = dns.update.Update(zone, keyring=keyring)
        up.delete(name, _type)
        up.add(name, ttl, _type, value)
        dns.query.tcp(up, server)
        keyring2 = dns.tsigkeyring.from_text({'otheri-key': 'AAFjaI4lkvXNkRAIExbFYA=='})
        up2 = dns.update.Update(zone, keyring=keyring2)
        up2.delete(name, _type)
        up2.add(name, ttl, _type, value)
        dns.query.tcp(up2, server)
    return "DNS replace {0} finish".format(name)


@celery.task(name='tasks.resolution_del')
def resolution_del(zone, name, _type, value):
    """删除DNS解析"""
    server = "10.96.5.96"
    if zone == "open.com.cn" and _type == 'A':
        if "10.100" in value or "10.96" in value:
            keyring = dns.tsigkeyring.from_text({'other-key': 'WWFjaI4lkvXNkRAIExbFYA=='})
            up = dns.update.Update(zone, keyring=keyring)
            up.delete(name, _type)
            dns.query.tcp(up, server)
            # for win AD
            server = "10.96.5.58"
            up = dns.update.Update(zone)
            up.delete(name, _type)
            dns.query.tcp(up, server)
        else:
            keyring = dns.tsigkeyring.from_text({'other-key': 'WWFjaI4lkvXNkRAIExbFYA=='})
            up = dns.update.Update(zone, keyring=keyring)
            up.delete(name, _type)
            dns.query.tcp(up, server)
            keyring2 = dns.tsigkeyring.from_text({'otheri-key': 'AAFjaI4lkvXNkRAIExbFYA=='})
            up2 = dns.update.Update(zone, keyring=keyring2)
            up2.delete(name, _type)
            dns.query.tcp(up2, server)
    else:
        keyring = dns.tsigkeyring.from_text({'other-key': 'WWFjaI4lkvXNkRAIExbFYA=='})
        up = dns.update.Update(zone, keyring=keyring)
        up.delete(name, _type)
        dns.query.tcp(up, server)
        keyring2 = dns.tsigkeyring.from_text({'otheri-key': 'AAFjaI4lkvXNkRAIExbFYA=='})
        up2 = dns.update.Update(zone, keyring=keyring2)
        up2.delete(name, _type)
        dns.query.tcp(up2, server)
    return "DNS del {0} finish".format(name)

