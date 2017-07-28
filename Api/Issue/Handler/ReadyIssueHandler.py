#coding=utf-8

from lib.urlmap import urlmap
from lib.basehandler import BaseHandler
from tornado import web,gen
from Issue.Entity.ReadyIssueModel import ReadyIssueServer
import json
from sqlalchemy import desc,or_,and_,engine
from Issue import tasks


@urlmap(r'/readyissue\/?([0-9]*)')
class ReadyHandler(BaseHandler):
    @web.asynchronous
    def get(self, ident):
        """获取预生产发布信息"""
        username = self.get_cookie("username")
        page = int(self.get_argument('page', 1))
        searchKey = self.get_argument('searchKey', None)
        pagesize = int(self.get_argument('pagesize', self._PageSize))
        totalquery = self.db.query(ReadyIssueServer.Id)
        NgIssueObj = self.db.query(ReadyIssueServer)
        if searchKey:
            totalquery = totalquery.filter(or_(ReadyIssueServer.DomainName.like('%%%s%%' % searchKey), ReadyIssueServer.HealthExam.like('%%%s%%' % searchKey), ReadyIssueServer.Port.like('%%%s%%' % searchKey)))
            NgIssueObj = NgIssueObj.filter(or_(ReadyIssueServer.DomainName.like('%%%s%%' % searchKey), ReadyIssueServer.HealthExam.like('%%%s%%' % searchKey), ReadyIssueServer.Port.like('%%%s%%' % searchKey)))
        self.Result['total'] = totalquery.count()
        serverTask = NgIssueObj.order_by(desc(ReadyIssueServer.Id)).limit(pagesize).offset((page - 1) * pagesize).all()
        self.Result['rows'] = list(map(lambda obj: obj.toDict(), serverTask))
        self.Result['username'] = username
        self.finish(self.Result)

    @web.asynchronous
    def post(self, ident=0):
        """预生产创建nginx及consul"""
        data = json.loads(self.request.body.decode("utf-8"))
        objTask = ReadyIssueServer()
        domainname = data['params'].get('DomainName', None)
        objTask.name = "".join(domainname.split("-"))
        objTask.DomainName = domainname + ".pdyf.open.com.cn"
        objTask.HealthExam = data['params'].get('HealthExam', None)
        objTask.Port = int(data['params'].get('Port', None))
        objTask.Publisher = self.get_cookie("username")
        self.db.add(objTask)
        self.db.commit()
        tasks.ready_issue.delay(objTask.name, objTask.Port, domainname, objTask.HealthExam)
        self.Result['rows'] = 1
        self.Result['info'] = u'创建成功'
        self.finish(self.Result)

    @web.asynchronous
    def delete(self, ident):
        """预生产删除nginx及consul"""
        pro = self.db.query(ReadyIssueServer).filter(ReadyIssueServer.Id==ident).first()
        domainname = pro.DomainName.split(".")[0]
        tasks.ready_issue_del.delay(domainname)
        self.db.query(ReadyIssueServer).filter(ReadyIssueServer.Id==ident).delete()
        self.db.commit()
        self.Result['info'] = u'删除nginx及consul成功'
        self.finish(self.Result)
