#coding=utf-8
from sqlalchemy import Column, Integer, String, Text, DateTime
from lib.Route import BaseModel, ResolutionModel


class ZoneServer(BaseModel, ResolutionModel):
    """
    Zone list
    """
    __tablename__ = 'bk_zone'

    Id = Column('fi_id', Integer, primary_key=True)
    ZoneName = Column('fs_zone_name', String(50))

    def toDict(self):
        return {
            'Id': self.Id,
            'ZoneName': self.ZoneName,
        }