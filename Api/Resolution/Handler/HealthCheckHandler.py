#coding=utf-8

from lib.urlmap import urlmap
from lib.basehandler import BaseHandler
from tornado import web, gen
from Resolution.Entity.HealthCheckModel import HealthCheckServer
import json
from sqlalchemy import desc, or_, and_, engine
from Resolution import tasks
import datetime
from apscheduler.schedulers.tornado import TornadoScheduler
import socket
import requests


@urlmap(r'/healthcheck\/?([0-9]*)')
class HealthCheckHandler(BaseHandler):
    @web.asynchronous
    def get(self, ident):
        """获取健康检查信息"""
        page = int(self.get_argument('page', 1))
        searchKey = self.get_argument('searchKey', None)
        pagesize = int(self.get_argument('pagesize', self._PageSize))
        totalquery = self.db.query(HealthCheckServer.Id)
        HealthCheckObj = self.db.query(HealthCheckServer)
        if searchKey:
            totalquery = totalquery.filter(HealthCheckServer.DomainName.like('%%%s%%' % searchKey))
            HealthCheckObj = HealthCheckObj.filter(HealthCheckServer.DomainName.like('%%%s%%' % searchKey))
        self.Result['total'] = totalquery.count()
        serverTask = HealthCheckObj.order_by(desc(HealthCheckServer.Id)).limit(pagesize).offset((page - 1) * pagesize).all()
        self.Result['rows'] = list(map(lambda obj: obj.toDict(), serverTask))
        self.finish(self.Result)

    def scheduler_add(self, domainname, checktype, recordvalue, checkport, checkurl):
        """创建健康检查任务"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
        requests.packages.urllib3.disable_warnings()
        pro = self.db.query(HealthCheckServer).filter(and_(HealthCheckServer.RecordValue == recordvalue,
                                                           HealthCheckServer.DomainName == domainname))
        status_value = pro.first()
        domainname_list = domainname.split('.')
        if domainname_list[-1] == 'cn':
            zonename = '.'.join(domainname_list[-3:])
            name = domainname_list[0:-3][0]
        else:
            zonename = '.'.join(domainname_list[-2:])
            name = domainname_list[0:-2][0]
        if checktype == 'tcp':
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.connect((recordvalue, int(checkport)))
                s.shutdown(2)
                if status_value.CheckStatus != 1:
                    pro.update({'CheckStatus': 1})
                    self.db.commit()
                    tasks.resolution.delay('10.96.140.61', zonename, name, 3600, 'A', recordvalue, 'add')
                    if name == 'www':
                        tasks.resolution.delay('10.96.140.61', zonename, "@", 3600, 'A', recordvalue, 'add')
                return '{0} is open'.format(checkport)
            except Exception:
                pro.update({'CheckStatus': 2})
                self.db.commit()
                tasks.resolution.delay('10.96.140.61', zonename, name, 3600, 'A', recordvalue, 'delete')
                if name == 'www':
                    tasks.resolution.delay('10.96.140.61', zonename, "@", 3600, 'A', recordvalue, 'delete')
                return '{0} is close'.format(checkport)
        elif checktype == 'http':
            url = 'http://{0}{1}'.format(recordvalue, checkurl)
            try:
                result = requests.get(url, headers=headers)
                if result.status_code == 200:
                    if status_value.CheckStatus != 1:
                        pro.update({'CheckStatus': 1})
                        self.db.commit()
                        tasks.resolution.delay('10.96.140.61', zonename, name, 3600, 'A', recordvalue, 'add')
                        if name == 'www':
                            tasks.resolution.delay('10.96.140.61', zonename, "@", 3600, 'A', recordvalue, 'add')
                    return 'healthcheck is ok'
            except Exception:
                pro.update({'CheckStatus': 2})
                self.db.commit()
                tasks.resolution.delay('10.96.140.61', zonename, name, 3600, 'A', recordvalue, 'delete')
                if name == 'www':
                    tasks.resolution.delay('10.96.140.61', zonename, "@", 3600, 'A', recordvalue, 'delete')
                return 'healthcheck is error'
        elif checktype == 'https':
            url = 'https://{0}{1}'.format(recordvalue, checkurl)
            try:
                result = requests.get(url, headers=headers, verify=False)
                if result.status_code == 200:
                    if status_value.CheckStatus != 1:
                        pro.update({'CheckStatus': 1})
                        self.db.commit()
                        tasks.resolution.delay('10.96.140.61', zonename, name, 3600, 'A', recordvalue, 'add')
                        if name == 'www':
                            tasks.resolution.delay('10.96.140.61', zonename, "@", 3600, 'A', recordvalue, 'add')
                    return 'healthcheck is ok'
            except Exception:
                pro.update({'CheckStatus': 2})
                self.db.commit()
                tasks.resolution.delay('10.96.140.61', zonename, name, 3600, 'A', recordvalue, 'delete')
                if name == 'www':
                    tasks.resolution.delay('10.96.140.61', zonename, "@", 3600, 'A', recordvalue, 'delete')
                return 'healthcheck is error'

    @web.asynchronous
    def post(self, ident):
        """创建健康检查"""
        data = json.loads(self.request.body.decode("utf-8"))
        objTask = HealthCheckServer()
        objTask.DomainName = data['params'].get('DomainName', None)
        objTask.RecordValue = data['params'].get('RecordValue', None)
        objTask.CheckType = data['params'].get('CheckType', None)
        objTask.CheckPort = data['params'].get('CheckPort', None)
        objTask.CheckUrl = data['params'].get('CheckUrl', None)
        objTask.CheckStatus = 1
        objTask.CheckCycle = data['params'].get('CheckCycle', None)
        objTask.Publisher = self.get_cookie("username")
        objTask.CreateTime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self.db.add(objTask)
        self.db.commit()
        scheduler = TornadoScheduler()
        scheduler.add_job(self.scheduler_add, 'interval',
                          seconds=objTask.CheckCycle,
                          kwargs={'domainname': objTask.DomainName, 'checktype': objTask.CheckType,
                                  'recordvalue': objTask.RecordValue, 'checkport': objTask.CheckPort, 'checkurl': objTask.CheckUrl})
        scheduler.start()
        self.Result['rows'] = 1
        self.Result['info'] = u'创建成功'
        self.finish(self.Result)

    @web.asynchronous
    def put(self, ident):
        """修改健康检查"""
        data = json.loads(self.request.body.decode("utf-8"))
        objTask = self.db.query(HealthCheckServer).get(ident)
        objTask.ZoneName = data['params'].get('ZoneName', None)
        objTask.Name = data['params'].get('Name', None)
        objTask.DomainName = objTask.Name + "." + objTask.ZoneName
        objTask.RecordType = data['params'].get('RecordType', None)
        objTask.RecordedValue = data['params'].get('RecordedValue', None)
        objTask.Publisher = self.get_cookie("username")
        objTask.CreateTime = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        self.db.add(objTask)
        self.db.commit()
        self.Result['rows'] = 1
        self.Result['info'] = u'修改成功'
        self.finish(self.Result)

    @web.asynchronous
    def delete(self, ident):
        """删除健康检查"""
        pro = self.db.query(HealthCheckServer).filter(HealthCheckServer.Id == ident).first()
        self.db.query(HealthCheckServer).filter(HealthCheckServer.Id == ident).delete()
        self.db.commit()
        self.Result['info'] = u'删除DNS解析成功'
        self.finish(self.Result)