#coding=utf-8
from sqlalchemy import Column, Integer, String, Text, DateTime
from lib.Route import BaseModel, HealthCheckModel
import datetime
from Resolution.Handler.functions import getStatusId


class HealthCheckServer(BaseModel, HealthCheckModel):
    """
    域名健康检查
    """
    __tablename__ = 'bk_healthcheck'

    Id = Column('fi_id', Integer, primary_key=True)
    DomainName = Column('fs_domain_name', String(50))
    RecordValue = Column('fs_record_value', String(50))
    CheckType = Column('fs_check_type', String(20))
    CheckPort = Column('fi_port', Integer)
    CheckUrl = Column('fs_check_url', String(30))
    CheckStatus = Column('fi_status_type', Integer)
    CheckCycle = Column('fi_check_cycle', Integer)  # 检查周期
    Publisher = Column('fs_publisher', String(50))
    CreateTime = Column('ft_create_time', DateTime, default=datetime.datetime.now())

    def toDict(self):
        return {
            'Id': self.Id,
            'DomainName': self.DomainName,
            'RecordValue': self.RecordValue,
            'CheckType': self.CheckType,
            'CheckPort': self.CheckPort,
            'CheckUrl': self.CheckUrl,
            'CheckStatus': getStatusId(self.CheckStatus),
            'StatusNum': self.CheckStatus,
            'CheckCycle': self.CheckCycle,
            'Publisher': self.Publisher,
            'CreateTime': self.CreateTime.strftime('%Y-%m-%d %H:%M:%S') if self.CreateTime else ''
        }