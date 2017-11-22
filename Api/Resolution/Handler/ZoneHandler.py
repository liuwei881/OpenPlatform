#coding=utf-8

from lib.urlmap import urlmap
from lib.basehandler import BaseHandler
from tornado import web,gen
from Resolution.Entity.ZoneModel import ZoneServer
import json


@urlmap(r'/zone/')
class ZoneHandler(BaseHandler):
    @web.asynchronous
    def get(self):
        """获取ZONE信息"""
        zone = self.db.query(ZoneServer).all()
        data = json.dumps(sorted([i.ZoneName for i in zone]), indent=2)
        self.finish(data)