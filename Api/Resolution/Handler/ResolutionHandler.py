#coding=utf-8

from lib.urlmap import urlmap
from lib.basehandler import BaseHandler
from tornado import web,gen
from Resolution.Entity.ResolutionModel import ResolutionServer
import json
from sqlalchemy import desc,or_,and_,engine
from Resolution import tasks
import datetime, time


@urlmap(r'/resolution\/?([0-9]*)')
class NgHandler(BaseHandler):
    @web.asynchronous
    def get(self, ident):
        """获取DNS解析信息"""
        username = self.get_cookie("username")
        page = int(self.get_argument('page', 1))
        searchKey = self.get_argument('searchKey', None)
        pagesize = int(self.get_argument('pagesize', self._PageSize))
        totalquery = self.db.query(ResolutionServer.Id)
        NgIssueObj = self.db.query(ResolutionServer)
        if searchKey:
            totalquery = totalquery.filter(ResolutionServer.DomainName.like('%%%s%%' % searchKey))
            NgIssueObj = NgIssueObj.filter(ResolutionServer.DomainName.like('%%%s%%' % searchKey))
        self.Result['total'] = totalquery.count()
        serverTask = NgIssueObj.order_by(desc(ResolutionServer.Id)).limit(pagesize).offset((page - 1) * pagesize).all()
        self.Result['rows'] = list(map(lambda obj: obj.toDict(), serverTask))
        self.Result['username'] = username
        self.finish(self.Result)

    @web.asynchronous
    def post(self, ident):
        """DNS解析操作"""
        data = json.loads(self.request.body.decode("utf-8"))
        objTask = ResolutionServer()
        objTask.ZoneName = data['params'].get('ZoneName', None)
        objTask.Name = data['params'].get('Name', None)
        if "*" in objTask.Name:
            objTask.Name = "*"
        objTask.DomainName = objTask.Name + "." + objTask.ZoneName
        objTask.RecordType = data['params'].get('RecordType', None)
        objTask.RecordedValue = data['params'].get('RecordedValue', None)
        objTask.Publisher = self.get_cookie("username")
        objTask.CreateTime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self.db.add(objTask)
        self.db.commit()
        # ttl = 3600
        tasks.resolution.delay('10.96.140.61', objTask.ZoneName, objTask.Name, 3600, objTask.RecordType,
                               objTask.RecordedValue, 'add')
        if objTask.Name == 'www':
            tasks.resolution.delay('10.96.140.61', objTask.ZoneName, "@", 3600, objTask.RecordType,
                                   objTask.RecordedValue, 'add')
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
