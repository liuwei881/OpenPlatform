#coding=utf-8

from lib.urlmap import urlmap
from lib.basehandler import BaseHandler
from tornado import web,gen
from Release.Entity.TcpReleaseModel import TcpReleaseServer
import json
from sqlalchemy import desc,or_,and_,engine
from Release import tasks
import datetime


@urlmap(r'/tcprelease\/?([0-9]*)')
class NgTcpHandler(BaseHandler):
    @web.asynchronous
    def get(self, ident):
        """获取TCP发布信息"""
        username = self.get_cookie("username")
        page = int(self.get_argument('page', 1))
        searchKey = self.get_argument('searchKey', None)
        pagesize = int(self.get_argument('pagesize', self._PageSize))
        totalquery = self.db.query(TcpReleaseServer.Id)
        NgTcpReleaseObj = self.db.query(TcpReleaseServer)
        if searchKey:
            totalquery = totalquery.filter(or_(TcpReleaseServer.DomainName.like('%%%s%%' % searchKey), TcpReleaseServer.Port.like('%%%s%%' % searchKey)))
            NgTcpReleaseObj = NgTcpReleaseObj.filter(or_(TcpReleaseServer.DomainName.like('%%%s%%' % searchKey), TcpReleaseServer.Port.like('%%%s%%' % searchKey)))
        self.Result['total'] = totalquery.count()
        serverTask = NgTcpReleaseObj.order_by(desc(TcpReleaseServer.Id)).limit(pagesize).offset((page - 1) * pagesize).all()
        self.Result['rows'] = list(map(lambda obj: obj.toDict(), serverTask))
        self.Result['username'] = username
        self.finish(self.Result)

    @web.asynchronous
    def post(self, ident=0):
        """创建nginx及consul"""
        data = json.loads(self.request.body.decode("utf-8"))
        objTask = TcpReleaseServer()
        domainname = data['params'].get('DomainName', None)
        objTask.DomainName = domainname + ".openkf.cn"
        objTask.Port = int(data['params'].get('Port', None))
        objTask.Publisher = self.get_cookie("username")
        objTask.CreateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.db.add(objTask)
        self.db.commit()
        tasks.tcp_release.delay(domainname, objTask.Port)
        tasks.dns_resolution.delay('add', domainname, 60, 'A', '10.100.138.135')
        self.Result['rows'] = 1
        self.Result['info'] = u'创建成功'
        self.finish(self.Result)

    @web.asynchronous
    def delete(self, ident):
        """删除nginx及consul"""
        pro = self.db.query(TcpReleaseServer).filter(TcpReleaseServer.Id == ident).first()
        domainname = pro.DomainName.split(".")[0]
        tasks.tcp_release_del.delay(domainname)
        tasks.dns_resolution.delay('delete', domainname, 60, 'A', '10.100.138.135')
        self.db.query(TcpReleaseServer).filter(TcpReleaseServer.Id == ident).delete()
        self.db.commit()
        self.Result['info'] = u'删除nginx及consul成功'
        self.finish(self.Result)
