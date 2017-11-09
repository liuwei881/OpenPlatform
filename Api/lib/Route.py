# -*- coding: utf-8 -*-
__author__ = 'liuwei'
__datetime__ = '17-4-1'

import random
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import desc
from lib.Extension import DataUpdateExtension
from yaml import load

BaseModel = declarative_base()


class Basebase(object):
    __mapper_args__ = {
        'extension': DataUpdateExtension()
    }
    __table_args__ = {
        'mysql_engine': 'innodb',
        'mysql_charset': 'utf8'
    }

    @classmethod
    def get_by_id(cls, ident):
        entity = db_session.query(cls).get(ident)
        db_session.close_all()
        return entity

    @classmethod
    def get_page_list(cls, page, pagesize):
        if hasattr(cls, 'CreateTime'):
            entitys = db_session.query(cls).order_by(desc(cls.CreateTime)).offset((page - 1) * pagesize).limit(
                pagesize).all()
        else:
            entitys = db_session.query(cls).offset((page - 1) * pagesize).limit(pagesize).all()

        db_session.close_all()
        return entitys

    @classmethod
    def get_count(cls):
        count = db_session.query(cls).count()
        db_session.close_all()
        return count

    @classmethod
    def get_by_list_id(cls, list):
        print(cls.__mapper__.primary_key)


class VmWareModel(Basebase):
    pass
# class KvmModel(Basebase):
#     pass


class PortalModel(Basebase):
    pass


class IssueModel(Basebase):
    pass


class ReadyIssueModel(Basebase):
    pass


class ResolutionModel(Basebase):
    pass

with open(os.path.join(os.path.dirname(__file__), 'config.yaml'), 'r') as f:
    yaml = load(f)

engines = {}
for item in yaml['engines'].items():
    engines[item[0]] = create_engine(item[1], pool_recycle=120, echo=True, max_overflow=0, pool_size=5)


class RoutingSession(Session):
    def get_bind(self, mapper=None, clause=None):
        if mapper and issubclass(mapper.class_, VmWareModel):
            return engines['vmware']
        elif mapper and issubclass(mapper.class_, PortalModel):
            return engines['portal']
        elif mapper and issubclass(mapper.class_, IssueModel):
            return engines['issue']
        elif mapper and issubclass(mapper.class_, ReadyIssueModel):
            return engines['readyissue']
        elif mapper and issubclass(mapper.class_, ResolutionModel):
            return engines['resolution']
        else:
            return engines[
                random.choice(['base'])
            ]

Session = sessionmaker(class_=RoutingSession, autocommit=False)
db_session = Session()
