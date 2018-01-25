#coding=utf-8
from sqlalchemy import Column, Integer, String, Text, DateTime
from lib.Route import BaseModel,TcpReleaseModel
import datetime


class TcpReleaseServer(BaseModel, TcpReleaseModel):
    """
    nginx 4层发布数据库
    """
    __tablename__ = 'bk_tcp_release'

    Id = Column('fi_id', Integer, primary_key=True)
    DomainName = Column('fs_name', String(10))
    Port = Column('fi_port', Integer)
    Publisher = Column('fs_publisher', String(50))
    CreateTime = Column('ft_create_time', DateTime, default=datetime.datetime.now())

    def toDict(self):
        return {
            'Id': self.Id,
            'DomainName': self.DomainName,
            'Port': self.Port,
            'Publisher': self.Publisher,
            'CreateTime': self.CreateTime.strftime('%Y-%m-%d %H:%M:%S') if self.CreateTime else ''
        }