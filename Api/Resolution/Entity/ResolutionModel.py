#coding=utf-8
from sqlalchemy import Column, Integer, String, Text, DateTime
from lib.Route import BaseModel,ResolutionModel
import datetime


class ResolutionServer(BaseModel, ResolutionModel):
    """
    Dns解析数据库
    """
    __tablename__ = 'bk_resolution'

    Id = Column('fi_id', Integer, primary_key=True)
    DomainName = Column('fs_domain_name', String(10))
    Ip = Column('fs_ip', String(50))
    Publisher = Column('fs_publisher', String(50))
    CreateTime = Column('ft_create_time', DateTime, default=datetime.datetime.now())

    def toDict(self):
        return {
            'Id': self.Id,
            'DomainName': self.DomainName,
            'Ip': self.Ip,
            'Publisher': self.Publisher,
            'CreateTime': self.CreateTime.strftime('%Y-%m-%d %H:%M:%S') if self.CreateTime else ''
        }