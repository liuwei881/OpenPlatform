#coding=utf-8
from sqlalchemy import Column, Integer, String, Text, DateTime
from lib.Route import BaseModel,PortalModel

class PortalServer(BaseModel,PortalModel):
    """
    portal入口数据库
    """
    __tablename__ = 'bk_portal'

    Id = Column('fi_id', Integer, primary_key=True)
    Name = Column('fs_name', String(10))
    Url = Column('fs_url', String(50))
    Icon = Column('fs_icon', String(255))

    def toDict(self):
        return {
            'Id': self.Id,
            'Name': self.Name,
            'Url': self.Url,
            'Icon': self.Icon
        }