# coding=utf-8

from lib.urlmap import urlmap
from lib.basehandler import BaseHandler
from tornado import web, gen
from VmWare.Entity.DataCenterModel import DataCenterList
import json


@urlmap(r'/datacenter/')
class DataCenterHandler(BaseHandler):
    """获取数据中心,集群,资源池三级联动"""
    @web.asynchronous
    def get(self):
        datacenter = self.db.query(DataCenterList).filter(
            DataCenterList.Level == 1)
        datacenter_list = []
        for i in datacenter:
            d = {}
            d["id"] = i.DataCenterId
            d["name"] = i.DataCenterName
            d["code"] = i.DataCenterId
            d["child"] = []
            child = self.db.query(DataCenterList).filter(
                DataCenterList.Level == 2, DataCenterList.Parent == i.DataCenterId)
            for c in child:
                grandchild = self.db.query(DataCenterList).filter(
                    DataCenterList.Level == 3, DataCenterList.Parent == c.DataCenterId)
                f = {
                    "id": c.DataCenterId,
                    "name": c.DataCenterName,
                    "grandchild": []}
                for j in grandchild:
                    f["grandchild"].append(
                        {"id": j.DataCenterId, "name": j.DataCenterName})
                    d["child"].append(f)
                    datacenter_list.append(d)
        r = []
        for i in datacenter_list:
            f = []
            for j in i["child"]:
                if j not in f:
                    f.append(j)
                    i["child"] = f
            r.append(i)
        rows = []
        [rows.append(i) for i in r if i not in rows]
        data = json.dumps(rows, indent=2)
        self.finish(data)