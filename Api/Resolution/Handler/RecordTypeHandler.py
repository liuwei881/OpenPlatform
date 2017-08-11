#coding=utf-8

from lib.urlmap import urlmap
from lib.basehandler import BaseHandler
from tornado import web,gen
from Resolution.Entity.RecordTypeModel import RecordTypeServer
import json


@urlmap(r'/recordtype/')
class RecordTypeHandler(BaseHandler):
    @web.asynchronous
    def get(self):
        """获取ZONE信息"""
        zone = self.db.query(RecordTypeServer).all()
        data = json.dumps([i.RecordType for i in zone], indent=2)
        self.finish(data)