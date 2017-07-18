#coding=utf-8

from sqlalchemy import Column, Integer, String, Text, DateTime
from lib.Route import BaseModel


class MirrorList(BaseModel):
    """
    三级联动镜像
    """
    __tablename__ = 'bk_mirrorname_list'
    MirrorId = Column('fi_id', Integer, primary_key=True)
    MirrorName = Column('fs_mirror_name', String(50))
    Level = Column('fi_level', Integer)
    Parent = Column('fi_parent', Integer)

    def toDict(self):
        return {
            'MirrorId': self.MirrorId,
            'MirrorName':self.MirrorName,
            'Level':self.Level,
            'Parent':self.Parent
        }