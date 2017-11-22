#coding=utf-8

from lib.urlmap import urlmap
from lib.basehandler import BaseHandler
from tornado import web,gen
import json, subprocess
from Resolution.Entity.ResolutionModel import ResolutionServer


@urlmap(r'/digtest\/?([0-9]*)')
class DigHandler(BaseHandler):
    @web.asynchronous
    def get(self, ident):
        """Dig测试"""
        zone = self.db.query(ResolutionServer).get(ident)
        if zone.RecordedValue.startswith('10.'):
            r = subprocess.check_output(['dig', '@10.98.91.11', '{0}'.format(zone.DomainName), '-y',
                                         'view_internal:i3XGCWmxZYgQdY91Tf52RA=='])
            result = r.decode('utf-8').split(';;')[7].replace('\t', ' ').replace('\n', ' ')
        else:
            r = subprocess.check_output(['dig', '@10.98.91.11', '{0}'.format(zone.DomainName), '-y',
                                         'default:XkAaeFO8EBX4ASrbaNN0lA=='])
            result = r.decode('utf-8').split(';;')[7].replace('\t', ' ').replace('\n', ' ')
        self.finish(result)