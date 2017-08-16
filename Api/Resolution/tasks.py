#coding=utf-8

from celery import Celery, task
import os
import dns.tsigkeyring
import dns.update
import dns.query
from fabric.api import *
import datetime


celery = Celery("tasks", broker="amqp://")
celery.conf.CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'amqp')
celery.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_RESULT_SERIALIZER='json',
    CELERY_ROUTES={
        'tasks.resolution': {'queue': 'resolution'},
    })


@celery.task(name='tasks.resolution')
def resolution(server, zone, name, ttl, _type, value, action):
    """添加DNS解析"""
    env.key_filename = "~/.ssh/id_rsa"
    if server == '10.96.5.96':
        def cp_zone(files):
            env.host_string = 'chenhy@10.96.5.96'
            with cd('/data/bind/zones'):
                sudo('cp {0} backup-conf/{1}.bak{2}'.format(files, files,
                                                            datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')))
        cp_zone('db.' + zone)
        cp_zone('db.' + zone + '-MD')
    elif server == '10.96.5.91':
        def cp_zone(files):
            env.host_string = 'root@10.96.5.91'
            with cd('/data/bind/zones'):
                run('cp {0} backup-conf/{1}.bak{2}'.format(files, files,
                                                            datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')))
        cp_zone('db.' + zone)
        cp_zone('db.' + zone + '-MD')

    if zone == "open.com.cn":
        if "10.100" in value or "10.96" in value or "10.191" in value:
            keyring = dns.tsigkeyring.from_text({'other-key': 'WWFjaI4lkvXNkRAIExbFYA=='})
            up = dns.update.Update(zone, keyring=keyring)
            server2 = "10.96.5.58"
            if action == 'add':
                up.add(name, ttl, _type, value)
                dns.query.tcp(up, server)
                # for win AD
                up2 = dns.update.Update(zone)
                up2.add(name, ttl, _type, value)
                dns.query.tcp(up, server2)
            elif action == 'change':
                up.delete(name, _type)
                up.add(name, ttl, _type, value)
                dns.query.tcp(up, server)
                # for win AD
                up2 = dns.update.Update(zone)
                up2.delete(name, _type)
                up2.add(name, ttl, _type, value)
                dns.query.tcp(up, server2)
            elif action == 'delete':
                up.delete(name, _type)
                dns.query.tcp(up, server)
                # for win AD
                up2 = dns.update.Update(zone)
                up2.delete(name, _type)
                dns.query.tcp(up2, server2)
        else:
            if _type == 'A':
                keyring2 = dns.tsigkeyring.from_text({'otheri-key': 'AAFjaI4lkvXNkRAIExbFYA=='})
                up2 = dns.update.Update(zone, keyring=keyring2)
                if action == 'add':
                    up2.add(name, ttl, _type, value)
                    dns.query.tcp(up2, server)
                elif action == 'change':
                    up2.delete(name, _type)
                    up2.add(name, ttl, _type, value)
                    dns.query.tcp(up2, server)
                elif action == 'delete':
                    up2.delete(name, _type)
                    dns.query.tcp(up2, server)
            else:
                keyring = dns.tsigkeyring.from_text({'other-key': 'WWFjaI4lkvXNkRAIExbFYA=='})
                up = dns.update.Update(zone, keyring=keyring)
                keyring2 = dns.tsigkeyring.from_text({'otheri-key': 'AAFjaI4lkvXNkRAIExbFYA=='})
                up2 = dns.update.Update(zone, keyring=keyring2)
                if action == 'add':
                    up.add(name, ttl, _type, value)
                    dns.query.tcp(up, server)
                    up2.add(name, ttl, _type, value)
                    dns.query.tcp(up2, server)
                elif action == 'change':
                    up.delete(name, _type)
                    up.add(name, ttl, _type, value)
                    dns.query.tcp(up, server)
                    up2.delete(name, _type)
                    up2.add(name, ttl, _type, value)
                    dns.query.tcp(up2, server)
                elif action == 'delete':
                    up.delete(name, _type)
                    dns.query.tcp(up, server)
                    up2.delete(name, _type)
                    dns.query.tcp(up2, server)
    else:
        if "10.100" in value or "10.96" in value or "10.191" in value:
            keyring = dns.tsigkeyring.from_text({'other-key': 'WWFjaI4lkvXNkRAIExbFYA=='})
            up = dns.update.Update(zone, keyring=keyring)
            if action == 'add':
                up.add(name, ttl, _type, value)
                dns.query.tcp(up, server)
            elif action == 'change':
                up.delete(name, _type)
                up.add(name, ttl, _type, value)
                dns.query.tcp(up, server)
            elif action == 'delete':
                up.delete(name, _type)
                dns.query.tcp(up, server)
        else:
            if _type == 'A':
                keyring2 = dns.tsigkeyring.from_text({'otheri-key': 'AAFjaI4lkvXNkRAIExbFYA=='})
                up2 = dns.update.Update(zone, keyring=keyring2)
                if action == 'add':
                    up2.add(name, ttl, _type, value)
                    dns.query.tcp(up2, server)
                elif action == 'change':
                    up2.delete(name, _type)
                    up2.add(name, ttl, _type, value)
                    dns.query.tcp(up2, server)
                elif action == 'delete':
                    up2.delete(name, _type)
                    dns.query.tcp(up2, server)
            else:
                keyring = dns.tsigkeyring.from_text({'other-key': 'WWFjaI4lkvXNkRAIExbFYA=='})
                up = dns.update.Update(zone, keyring=keyring)
                keyring2 = dns.tsigkeyring.from_text({'otheri-key': 'AAFjaI4lkvXNkRAIExbFYA=='})
                up2 = dns.update.Update(zone, keyring=keyring2)
                if action == 'add':
                    up.add(name, ttl, _type, value)
                    dns.query.tcp(up, server)
                    up2.add(name, ttl, _type, value)
                    dns.query.tcp(up2, server)
                elif action == 'change':
                    up.delete(name, _type)
                    up.add(name, ttl, _type, value)
                    dns.query.tcp(up, server)
                    up2.delete(name, _type)
                    up2.add(name, ttl, _type, value)
                    dns.query.tcp(up2, server)
                elif action == 'delete':
                    up.delete(name, _type)
                    dns.query.tcp(up, server)
                    up2.delete(name, _type)
                    dns.query.tcp(up2, server)
    return "DNS update {0} finish".format(name)
