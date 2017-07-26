#coding=utf-8

from lib.urlmap import urlmap
from lib.basehandler import BaseHandler
from tornado import web,gen
from Resolution.Entity.ResolutionModel import ResolutionServer
import json
from sqlalchemy import desc,or_,and_,engine


@urlmap(r'/resolution\/?([0-9]*)')
class NgHandler(BaseHandler):
    @web.asynchronous
    def get(self, ident):
        """获取发布信息"""
        username = self.get_cookie("username")
        page = int(self.get_argument('page', 1))
        searchKey = self.get_argument('searchKey', None)
        pagesize = int(self.get_argument('pagesize', self._PageSize))
        totalquery = self.db.query(ResolutionServer.Id)
        NgIssueObj = self.db.query(ResolutionServer)
        if searchKey:
            totalquery = totalquery.filter(or_(ResolutionServer.DomainName.like('%%%s%%' % searchKey), ResolutionServer.Ip.like('%%%s%%' % searchKey)))
            NgIssueObj = NgIssueObj.filter(or_(ResolutionServer.DomainName.like('%%%s%%' % searchKey), ResolutionServer.Ip.like('%%%s%%' % searchKey)))
        self.Result['total'] = totalquery.count()
        serverTask = NgIssueObj.order_by(desc(ResolutionServer.Id)).limit(pagesize).offset((page - 1) * pagesize).all()
        self.Result['rows'] = list(map(lambda obj: obj.toDict(), serverTask))
        self.Result['username'] = username
        self.finish(self.Result)

    @web.asynchronous
    def post(self, ident):
        pass

    @web.asynchronous
    def put(self, ident):
        pass

    @web.asynchronous
    def delete(self, ident):
        """删除nginx及consul"""
        # pro = self.db.query(IssueServer).filter(IssueServer.Id==ident).first()
        # domainname = pro.DomainName.split(".")[0]
        # tasks.issue_del.delay(domainname)
        # self.db.query(IssueServer).filter(IssueServer.Id==ident).delete()
        # self.db.commit()
        # self.Result['info'] = u'删除虚拟机成功'
        # self.finish(self.Result)
        pass
