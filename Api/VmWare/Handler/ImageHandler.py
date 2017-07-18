#coding=utf-8

from lib.urlmap import urlmap
from lib.basehandler import BaseHandler
from tornado import web,gen
from VmWare.Entity.ImageModel import MirrorList
import json


#获取镜像，三级联动
@urlmap(r'/mirror/')
class MirrorHandler(BaseHandler):
    @web.asynchronous
    def get(self):
        mirror = self.db.query(MirrorList).filter(MirrorList.Level==1)
        mirror_list = []
        for i in mirror:
            d = {}
            d["id"] = i.MirrorId
            d["name"] = i.MirrorName
            d["code"] = i.MirrorId
            d["child"] = []
            child = self.db.query(MirrorList).filter(MirrorList.Level==2,MirrorList.Parent==i.MirrorId)
            for c in child:
                d["child"].append({"id":c.MirrorId,"name":c.MirrorName,"child":[]})
                mirror_list.append(d)
        rows = []
        [rows.append(i) for i in mirror_list if i not in rows]
        data = json.dumps(rows,indent=2)
        self.finish(data)