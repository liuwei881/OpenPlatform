#coding=utf-8
from sqlalchemy import Column, Integer, String, Text, DateTime
from lib.Route import BaseModel, ResolutionModel


class RecordTypeServer(BaseModel, ResolutionModel):
    """
    record type
    """
    __tablename__ = 'bk_record_type'

    Id = Column('fi_id', Integer, primary_key=True)
    RecordType = Column('fs_record_type', String(50))

    def toDict(self):
        return {
            'Id': self.Id,
            'RecordType': self.RecordType,
        }