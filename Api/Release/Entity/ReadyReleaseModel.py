#coding=utf-8
from sqlalchemy import Column, Integer, String, Text, DateTime
from lib.Route import BaseModel,ReadyReleaseModel
import datetime


class ReadyReleaseServer(BaseModel, ReadyReleaseModel):
    """
    nginx预生产发布数据库
    """
    __tablename__ = 'bk_ready_release'

    Id = Column('fi_id', Integer, primary_key=True)
    Name = Column('fs_name', String(10))
    DomainName = Column('fs_domain_name', String(10))
    HealthExam = Column('fs_url', String(50))
    Port = Column('fi_port', Integer)
    Publisher = Column('fs_publisher', String(50))
    CreateTime = Column('ft_create_time', DateTime, default=datetime.datetime.now())

    def toDict(self):
        return {
            'Id': self.Id,
            'Name' : self.Name,
            'DomainName': self.DomainName,
            'HealthExam': self.HealthExam,
            'Port': self.Port,
            'Publisher': self.Publisher,
            'CreateTime': self.CreateTime.strftime('%Y-%m-%d %H:%M:%S') if self.CreateTime else ''
        }