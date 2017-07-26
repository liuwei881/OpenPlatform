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
    ZoneName = Column('fs_zone_name', String(50))
    DomainName = Column('fs_domain_name', String(50))
    RecordType = Column('fs_record_type', String(20))
    RecordedValue = Column('fs_record_value', String(50))
    Publisher = Column('fs_publisher', String(50))
    CreateTime = Column('ft_create_time', DateTime, default=datetime.datetime.now())

    def toDict(self):
        return {
            'Id': self.Id,
            'ZoneName': self.ZoneName,
            'DomainName': self.DomainName,
            'RecordType': self.RecordType,
            'RecordedValue': self.RecordedValue,
            'Publisher': self.Publisher,
            'CreateTime': self.CreateTime.strftime('%Y-%m-%d %H:%M:%S') if self.CreateTime else ''
        }