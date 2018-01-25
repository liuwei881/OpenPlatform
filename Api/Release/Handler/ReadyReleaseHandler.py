#coding=utf-8

from lib.urlmap import urlmap
from lib.basehandler import BaseHandler
from tornado import web,gen
from Release.Entity.ReadyReleaseModel import ReadyReleaseServer
import json
from sqlalchemy import desc,or_,and_,engine
from Release import tasks


@urlmap(r'/readyrelease\/?([0-9]*)')
class ReadyHandler(BaseHandler):
    @web.asynchronous
    def get(self, ident):
        """获取预生产发布信息"""
        username = self.get_cookie("username")
        page = int(self.get_argument('page', 1))
        searchKey = self.get_argument('searchKey', None)
        pagesize = int(self.get_argument('pagesize', self._PageSize))
        totalquery = self.db.query(ReadyReleaseServer.Id)
        NgReleaseObj = self.db.query(ReadyReleaseServer)
        if searchKey:
            totalquery = totalquery.filter(or_(ReadyReleaseServer.DomainName.like('%%%s%%' % searchKey), ReadyReleaseServer.HealthExam.like('%%%s%%' % searchKey), ReadyReleaseServer.Port.like('%%%s%%' % searchKey)))
            NgReleaseObj = NgReleaseObj.filter(or_(ReadyReleaseServer.DomainName.like('%%%s%%' % searchKey), ReadyReleaseServer.HealthExam.like('%%%s%%' % searchKey), ReadyReleaseServer.Port.like('%%%s%%' % searchKey)))
        self.Result['total'] = totalquery.count()
        serverTask = NgReleaseObj.order_by(desc(ReadyReleaseServer.Id)).limit(pagesize).offset((page - 1) * pagesize).all()
        self.Result['rows'] = list(map(lambda obj: obj.toDict(), serverTask))
        self.Result['username'] = username
        self.finish(self.Result)

    @web.asynchronous
    def post(self, ident=0):
        """预生产创建nginx及consul"""
        data = json.loads(self.request.body.decode("utf-8"))
        objTask = ReadyReleaseServer()
        domainname = data['params'].get('DomainName', None)
        objTask.name = "".join(domainname.split("-"))
        objTask.DomainName = domainname + ".pdyf.open.com.cn"
        objTask.HealthExam = data['params'].get('HealthExam', None)
        objTask.Port = int(data['params'].get('Port', None))
        objTask.Publisher = self.get_cookie("username")
        self.db.add(objTask)
        self.db.commit()
        tasks.ready_Release.delay(objTask.name, objTask.Port, domainname, objTask.HealthExam)
        self.Result['rows'] = 1
        self.Result['info'] = u'创建成功'
        self.finish(self.Result)

    @web.asynchronous
    def delete(self, ident):
        """预生产删除nginx及consul"""
        pro = self.db.query(ReadyReleaseServer).filter(ReadyReleaseServer.Id==ident).first()
        domainname = pro.DomainName.split(".")[0]
        tasks.ready_Release_del.delay(domainname)
        self.db.query(ReadyReleaseServer).filter(ReadyReleaseServer.Id==ident).delete()
        self.db.commit()
        self.Result['info'] = u'删除nginx及consul成功'
        self.finish(self.Result)
