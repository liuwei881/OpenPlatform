#coding=utf-8

from celery import Celery, task
import os
import dns.tsigkeyring
import dns.update
import dns.query
import datetime
import requests
import json

requests.packages.urllib3.disable_warnings()
#celery = Celery("tasks", broker="amqp://")
celery = Celery("tasks", broker="amqp://admin:open@2018@rabbitmq.sysgroup.open.com.cn:5672//")
celery.conf.CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'amqp')


celery.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_RESULT_SERIALIZER='json',
    CELERY_ROUTES={
        'tasks.resolution': {'queue': 'resolution'},
    })


def view_internal(view, zone, name, _type, value, action):
    """内网解析"""
    url = 'https://10.98.91.11:20120/views/{0}/zones/{1}/rrs'.format(view, zone)
    if action == 'add':
        payload = {
            'name': '{}'.format(name),
            'type': '{}'.format(_type),
            'ttl': '3600',
            'rdata': ['{}'.format(value)],
            'is_enable': 'yes',
            'expire_is_enable': 'no',
            'current_user': 'liuwei'}
        headers = {'Content-type': 'application/json'}
        r = requests.post(url, auth=('liuwei', 'Liuwei@2017'), data=json.dumps(payload),
                          headers=headers, verify=False)
        return r.text
    elif action == 'delete':
        payload = {
            'extend_ids': ['{0}${1}${2}'.format(name, _type, value)],
            'current_user': "liuwei"}
        headers = {'Content-type': 'application/json'}
        requests.delete(url, auth=('liuwei', 'Liuwei@2017'), data=json.dumps(payload),
                            headers=headers, verify=False)
        return {'ip': '{}'.format(value), 'name': '{}'.format('.'.join([name, zone]) + '.')}


def default(view, zone, name, _type, value, action):
    """外网解析"""
    url = 'https://10.98.91.11:20120/views/{0}/zones/{1}/rrs'.format(view, zone)
    if action == 'add':
        if _type == 'A':
            payload = {
                'name': '{}'.format(name),
                'type': '{}'.format(_type),
                'ttl': '3600',
                'rdata': ['{}'.format(value)],
                'is_enable': 'yes',
                'expire_is_enable': 'no',
                'current_user': 'liuwei'}
        else:
            payload = {
                'name': '{}'.format(name),
                'type': '{}'.format(_type),
                'ttl': '3600',
                'rdata': '{}'.format(value),
                'is_enable': 'yes',
                'expire_is_enable': 'no',
                'current_user': 'liuwei'}
        headers = {'Content-type': 'application/json'}
        r = requests.post(url, auth=('liuwei', 'Liuwei@2017'), data=json.dumps(payload),
                          headers=headers, verify=False)
        return r.text
    elif action == 'delete':
        payload = {
            'extend_ids': ['{0}${1}${2}'.format(name, _type, value)],
            'current_user': "liuwei"}
        headers = {'Content-type': 'application/json'}
        requests.delete(url, auth=('liuwei', 'Liuwei@2017'), data=json.dumps(payload),
                        headers=headers, verify=False)
        return {'ip': '{}'.format(value), 'name': '{}'.format('.'.join([name, zone]) + '.')}


def result_to_cmdb(result, action):
    """将结果传入cmdb"""
    import urllib.request
    import urllib.parse
    if action == 'delete':
        url = "http://10.100.17.175:5555/business/dns/delDNS"
        data = urllib.parse.urlencode(result).encode(encoding='UTF8')
    else:
        url = "http://10.100.17.175:5555/business/dns/addDNS"
        data = urllib.parse.urlencode({'dnsJson': '{}'.format(result)}).encode(encoding='UTF8')
    request = urllib.request.Request(url)
    request.add_header("Content-Type", "application/x-www-form-urlencoded;charset=utf-8")
    urllib.request.urlopen(request, data)
    return result


@celery.task(name='tasks.resolution')
def resolution(server, zone, name, ttl, _type, value, action):
    """添加DNS解析"""
    if zone == "open.com.cn":
        view = 'default'
        up = dns.update.Update(zone)
        if '10.100' in value or '10.96' in value or '10.98' in value:
            if action == 'add':
                up.add(name, ttl, _type, value)
                dns.query.tcp(up, server)
                result = {
                    "id": "{}".format('$'.join([_type, name, value, zone])),
                    "href": "",
                    "is_shared": "",
                    "state": "",
                    "name": "{}".format('.'.join([name, zone]) + '.'),
                    "type": "{}".format(_type),
                    "klass": "IN",
                    "ttl": 3600,
                    "rdata": "{}".format(value),
                    "reverse_name": "",
                    "is_enable": "yes",
                    "row_id": '',
                    "comment": "",
                    "audit_status": "",
                    "expire_time": "",
                    "expire_style": "",
                    "create_time": "{}".format(datetime.datetime.now().strftime('%Y-%m-%d')),
                    "expire_is_enable": "no"
                }
                result_to_cmdb(result, action)
            elif action == 'change':
                up.delete(name, _type)
                up.add(name, ttl, _type, value)
                dns.query.tcp(up, server)
                result = {
                    "id": "{}".format('$'.join([_type, name, value, zone])),
                    "href": "",
                    "is_shared": "",
                    "state": "",
                    "name": "{}".format('.'.join([name, zone]) + '.'),
                    "type": "{}".format(_type),
                    "klass": "IN",
                    "ttl": 3600,
                    "rdata": "{}".format(value),
                    "reverse_name": "",
                    "is_enable": "yes",
                    "row_id": '',
                    "comment": "",
                    "audit_status": "",
                    "expire_time": "",
                    "expire_style": "",
                    "create_time": "{}".format(datetime.datetime.now().strftime('%Y-%m-%d')),
                    "expire_is_enable": "no"
                }
                result_to_cmdb(result, action)
            elif action == 'delete':
                up.delete(name, _type)
                dns.query.tcp(up, server)
                result = {'ip': '{}'.format(value), 'name': '{}'.format('.'.join([name, zone]) + '.')}
                result_to_cmdb(result, action)
        elif _type == 'CNAME':
            if action == 'add':
                up.add(name, ttl, _type, value)
                dns.query.tcp(up, server)
                result = default(view, zone, name, _type, value, action)
                result_to_cmdb(result, action)
            elif action == 'change':
                up.delete(name, _type)
                up.add(name, ttl, _type, value)
                dns.query.tcp(up, server)
                result = default(view, zone, name, _type, value, action)
                result_to_cmdb(result, action)
            elif action == 'delete':
                up.delete(name, _type)
                dns.query.tcp(up, server)
                result = default(view, zone, name, _type, value, action)
                result_to_cmdb(result, action)
        else:
            return default(view, zone, name, _type, value, action)
    elif '10.100' in value or '10.96' in value or '10.98' in value:
        view = 'view_internal'
        result = view_internal(view, zone, name, _type, value, action)
        result_to_cmdb(result, action)
    else:
        view = 'default'
        result = default(view, zone, name, _type, value, action)
        result_to_cmdb(result, action)