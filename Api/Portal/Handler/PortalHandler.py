#coding=utf-8

from lib.urlmap import urlmap
from lib.basehandler import BaseHandler
from tornado import web,gen
from Portal.Entity.PortalModel import PortalServer
import json
from sqlalchemy import desc,or_,and_,engine


#入口
@urlmap(r'/protal\/?([0-9]*)')
class ProtalHandler(BaseHandler):
    @web.asynchronous
    def get(self, ident):
        username = self.get_cookie('username')
        server = self.db.query(PortalServer)
        if username == 'liuweia':
            serverTask = server.filter(PortalServer.Name != "权限不足").all()
        elif username == 'liuzhizheng':
            serverTask = server.filter(and_(PortalServer.Name == "虚拟机管理", PortalServer.Name == "DNS解析")).all()
        else:
            serverTask = server.filter(PortalServer.Name == "权限不足").all()
        self.Result['rows'] = list(map(lambda obj: obj.toDict(), serverTask))
        self.finish(self.Result)


