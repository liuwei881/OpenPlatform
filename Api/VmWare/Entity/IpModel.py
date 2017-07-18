#coding=utf-8
from sqlalchemy import Column, Integer
from lib.Route import BaseModel

class IpPool(BaseModel):
    """
    ip列表
    """
    __tablename__ = 'bk_ip_list'

    IpId = Column('fi_id', Integer, primary_key=True)
    Ip = Column('fi_ip', Integer)

    def toDict(self):
        return {
            'IpId': self.IpId,                  #id
            'Ip':self.Ip,               		#ip地址，用整型存储
        }