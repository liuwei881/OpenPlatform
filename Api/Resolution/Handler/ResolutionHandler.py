#coding=utf-8

from lib.urlmap import urlmap
from lib.basehandler import BaseHandler
from tornado import web, gen
from Resolution.Entity.ResolutionModel import ResolutionServer
import json
from sqlalchemy import desc,or_,and_,engine
from Resolution import tasks
import datetime, time


@urlmap(r'/resolution\/?([0-9]*)')
class DnsHandler(BaseHandler):
    @web.asynchronous
    def get(self, ident):
        """获取DNS解析信息"""
        username = self.get_cookie("username")
        page = int(self.get_argument('page', 1))
        searchKey = self.get_argument('searchKey', None)
        pagesize = int(self.get_argument('pagesize', self._PageSize))
        totalquery = self.db.query(ResolutionServer.Id)
        DnsIssueObj = self.db.query(ResolutionServer)
        if searchKey:
            totalquery = totalquery.filter(or_(ResolutionServer.DomainName.like('%%%s%%' % searchKey),
                                               ResolutionServer.RecordedValue.like('%%%s%%' % searchKey)))
            DnsIssueObj = DnsIssueObj.filter(or_(ResolutionServer.DomainName.like('%%%s%%' % searchKey),
                                                 ResolutionServer.RecordedValue.like('%%%s%%' % searchKey)))
        self.Result['total'] = totalquery.count()
        serverTask = DnsIssueObj.order_by(desc(ResolutionServer.Id)).limit(pagesize).offset((page - 1) * pagesize).all()
        DnsIssueObj.filter(ResolutionServer.Status == 1).update({
            'Status': 0,
        }, synchronize_session='fetch')
        self.db.commit()
        self.Result['rows'] = list(map(lambda obj: obj.toDict(), serverTask))
        self.Result['username'] = username
        self.finish(self.Result)

    @web.asynchronous
    def post(self, ident):
        """DNS解析操作"""
        data = json.loads(self.request.body.decode("utf-8"))
        objTask = ResolutionServer()
        data_dict = data['params'].get('RecordedValue', None)
        objTask.ZoneName = data['params'].get('ZoneName', None)
        objTask.Name = data['params'].get('Name', None)
        if "*" in objTask.Name:
            objTask.Name = "*"
        objTask.DomainName = objTask.Name + "." + objTask.ZoneName
        objTask.RecordType = data['params'].get('RecordType', None)
        objTask.Publisher = self.get_cookie("username")
        objTask.CreateTime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        # ttl = 3600
        for record in data_dict.values():
            objTask.RecordedValue = record
            pro = ResolutionServer(
                ZoneName=objTask.ZoneName,
                Name=objTask.Name,
                DomainName=objTask.DomainName,
                RecordType=objTask.RecordType,
                RecordedValue=record,
                Status=0,
                Publisher=objTask.Publisher,
                CreateTime=objTask.CreateTime
            )
            tasks.resolution.delay('10.96.140.61', objTask.ZoneName, objTask.Name, 3600, objTask.RecordType,
                                   objTask.RecordedValue, 'add')
            if objTask.Name == 'www':
                tasks.resolution.delay('10.96.140.61', objTask.ZoneName, "@", 3600, objTask.RecordType,
                                       objTask.RecordedValue, 'add')
            self.db.add(pro)
            self.db.commit()
        self.Result['rows'] = 1
        self.Result['info'] = u'创建成功'
        self.finish(self.Result)

    @web.asynchronous
    def put(self, ident):
        """修改DNS解析"""
        data = json.loads(self.request.body.decode("utf-8"))
        objTaskOld = self.db.query(ResolutionServer).get(ident)
        # put 删除原解析
        tasks.resolution.delay('10.96.140.61', objTaskOld.ZoneName, objTaskOld.Name, 3600,
                               objTaskOld.RecordType, objTaskOld.RecordedValue, 'delete')
        time.sleep(1)
        self.db.query(ResolutionServer).filter(ResolutionServer.Id == ident).delete()
        objTask = ResolutionServer()
        objTask.ZoneName = data['params'].get('ZoneName', None)
        objTask.Name = data['params'].get('Name', None)
        if "*" in objTask.Name:
            objTask.Name = "*"
        objTask.DomainName = objTask.Name + "." + objTask.ZoneName
        objTask.RecordType = data['params'].get('RecordType', None)
        objTask.RecordedValue = data['params'].get('RecordedValue', None)
        objTask.Publisher = self.get_cookie("username")
        objTask.CreateTime = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        self.db.add(objTask)
        # ttl = 3600
        tasks.resolution.delay('10.96.140.61', objTask.ZoneName, objTask.Name, 3600, objTask.RecordType,
                               objTask.RecordedValue, 'add')
        if objTask.Name == 'www':
            tasks.resolution.delay('10.96.140.61', objTask.ZoneName, "@", 3600, objTask.RecordType,
                                   objTask.RecordedValue, 'add')
        self.db.commit()
        self.Result['rows'] = 1
        self.Result['info'] = u'修改成功'
        self.finish(self.Result)

    @web.asynchronous
    def delete(self, ident):
        """删除DNS解析"""
        pro = self.db.query(ResolutionServer).filter(ResolutionServer.Id == ident).first()
        tasks.resolution.delay('10.96.140.61', pro.ZoneName, pro.Name, 3600,
                               pro.RecordType, pro.RecordedValue, 'delete')
        self.db.query(ResolutionServer).filter(ResolutionServer.Id == ident).delete()
        self.db.commit()
        self.Result['info'] = u'删除DNS解析成功'
        self.finish(self.Result)


@urlmap(r'/getinfo/')
class InfoHandler(BaseHandler):
    @web.asynchronous
    def get(self):
        """获取DNS统计信息"""
        result_record = []
        Now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        Before = (datetime.datetime.now() - datetime.timedelta(days=5)).strftime("%Y-%m-%d %H:%M:%S")
        totalquery = self.db.query(ResolutionServer)
        datetimequery = totalquery.filter(and_(ResolutionServer.CreateTime < Now,
                                               ResolutionServer.CreateTime > Before))
        zone_list = [(k.CreateTime.strftime('%Y-%m-%d'), k.ZoneName) for k in datetimequery]
        zone_list_only = sorted(set(zone_list))
        zone_name = set([k.ZoneName for k in datetimequery])
        for i in zone_name:
            record_dict = {}
            record_dict['name'] = i
            record_dict['data'] = []
            for j in zone_list_only:
                if j[1] == i:
                    record_dict['data'].append(zone_list.count(j))
                else:
                    record_dict['data'].append(0)
            result_record.append(record_dict)
        self.Result['datetime'] = list(map(lambda x: x[0], list(zone_list_only)))
        self.Result['data'] = result_record
        self.finish(self.Result)


@urlmap(r'/resolv/')
class ResolvHandler(BaseHandler):
    @web.asynchronous
    def get(self):
        """获取checkbox信息"""
        resolvTask = self.db.query(ResolutionServer).filter(ResolutionServer.Status == 1).all()
        self.Result['rows'] = list(map(lambda obj: (obj.DomainName, obj.RecordedValue), resolvTask))
        self.Result['all'] = list(map(lambda obj: obj.toDict(), resolvTask))
        self.Result['status'] = 200
        self.Result['info'] = u'修改成功'
        self.finish(self.Result)


@urlmap(r'/status\/?(.*)')
class StatusHandler(BaseHandler):
    """获取每列的Status"""
    @web.asynchronous
    def get(self, ident):
        if ident:
            objTask = self.db.query(ResolutionServer).get(ident)
            self.Result['rows'] = objTask.toDict()
        else:
            page = int(self.get_argument('page', 1))
            pagesize = int(self.get_argument('pagesize', self._PageSize))
            serverTask = self.db.query(ResolutionServer).order_by(desc(ResolutionServer.Id)).\
                limit(pagesize).offset((page - 1) * pagesize).all()
            self.Result['rows'] = list(map(lambda obj: obj.toDict(), serverTask))
        self.finish(self.Result)

    @web.asynchronous
    def put(self, ident):
        data = json.loads(self.request.body.decode("utf-8"))
        objTask = self.db.query(ResolutionServer).get(ident)
        Status = data['params'].get('Status', None)
        if Status == 0:
            objTask.Status = 1
        else:
            objTask.Status = 0
        self.db.add(objTask)
        self.db.commit()
        self.Result['rows'] = 1
        self.Result['status'] = objTask.Status
        self.Result['info'] = u'修改成功'
        self.finish(self.Result)