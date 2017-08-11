#coding=utf-8

from lib.urlmap import urlmap
from lib.basehandler import BaseHandler
from tornado import web,gen
from Resolution.Entity.ResolutionModel import ResolutionServer
import json
from sqlalchemy import desc,or_,and_,engine
from Resolution import tasks


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
        self.db.add(objTask)
        self.db.commit()
        # ttl = 21600
        tasks.resolution.delay(objTask.ZoneName, objTask.Name, 21600, objTask.RecordType, objTask.RecordedValue)
        if objTask.Name == 'www':
            tasks.resolution.delay(objTask.ZoneName, "@", 21600, objTask.RecordType, objTask.RecordedValue)
        self.Result['rows'] = 1
        self.Result['info'] = u'创建成功'
        self.finish(self.Result)

    @web.asynchronous
    def put(self, ident):
        """修改DNS解析"""
        data = json.loads(self.request.body.decode("utf-8"))
        objTask = self.db.query(ResolutionServer).get(ident)
        if ident and objTask:
            objTask.ZoneName = data['params'].get('ZoneName', None)
            objTask.Name = data['params'].get('Name', None)
            if "*" in objTask.Name:
                objTask.Name = "*"
            objTask.DomainName = objTask.Name + "." + objTask.ZoneName
            objTask.RecordType = data['params'].get('RecordType', None)
            objTask.RecordedValue = data['params'].get('RecordedValue', None)
            objTask.Publisher = self.get_cookie("username")
            self.db.add(objTask)
            self.db.commit()
            # ttl = 21600
            tasks.resolution_edit.delay(objTask.ZoneName, objTask.Name, 21600, objTask.RecordType,
                                        objTask.RecordedValue)
            if objTask.Name == 'www':
                tasks.resolution_edit.delay(objTask.ZoneName, "@", 21600, objTask.RecordType,
                                            objTask.RecordedValue)
            self.Result['rows'] = 1
            self.Result['info'] = u'修改成功'
        else:
            self.Result['rows'] = 0
            self.Result['info'] = u'修改失败'
        self.finish(self.Result)

    @web.asynchronous
    def delete(self, ident):
        """删除DNS解析"""
        pro = self.db.query(ResolutionServer).filter(ResolutionServer.Id == ident).first()
        name = pro.Name
        zone = pro.ZoneName
        _type = pro.RecordType
        value = pro.RecordedValue
        tasks.resolution_del.delay(zone, name, _type, value)
        self.db.query(ResolutionServer).filter(ResolutionServer.Id == ident).delete()
        self.db.commit()
        self.Result['info'] = u'删除DNS解析成功'
        self.finish(self.Result)
