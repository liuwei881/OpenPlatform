# coding=utf-8

from sqlalchemy import Column, Integer, String, Text, DateTime
from lib.Route import BaseModel


class DataCenterList(BaseModel):
    """
    三级联动数据中心,集群,资源池
    """
    __tablename__ = 'bk_datacenter_list'
    DataCenterId = Column('fi_id', Integer, primary_key=True)
    DataCenterName = Column('fs_datacenter_name', String(50))
    Level = Column('fi_level', Integer)
    Parent = Column('fi_parent', Integer)

    def toDict(self):
        return {
            'DataCenterId': self.DataCenterId,
            'DataCenterName': self.DataCenterName,
            'Level': self.Level,
            'Parent': self.Parent
        }
