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
        if username == 'admin':
            serverTask = self.db.query(PortalServer).all()
        else:
            serverTask = self.db.query(PortalServer).filter(PortalServer.Name != "系统维护").all()
        self.Result['rows'] = list(map(lambda obj: obj.toDict(), serverTask))
        self.finish(self.Result)
