#coding=utf-8
from sqlalchemy import Column, Integer, String, Text, DateTime
from lib.Route import BaseModel


class IdPool(BaseModel):
    """
    虚拟机ID池
    """
    __tablename__ = 'bk_id_pool'

    Id = Column('fi_id', Integer, primary_key=True)
    IdPool = Column('fi_idpool', Integer)

    def toDict(self):
        return {
            'Id': self.Id,                      #id
            'IdPool': self.IdPool               #id池
        }




