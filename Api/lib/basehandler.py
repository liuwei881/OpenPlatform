# -*- coding: utf-8 -*-
__author__ = 'liuwei'
__datetime__ = '17-4-1'

import tornado
import json
from lib.RedisCache import RightsCache

class CurrentUser(object):
    def __init__(self, uid=None):
        self.Uid = uid

_Current_User = CurrentUser(None)


class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, *argc, **argkw):
        super(BaseHandler, self).__init__(*argc, **argkw)

        _Current_User.Uid = self.get_current_user()
        self._PageSize = 15
        self.Result = {'status': 200, 'rows': [], 'total': 0, 'info': 'ok'}

    @property
    def db(self):
        return self.application.db

    @property
    def Redis(self):
        return self.application.Redis

    @property
    def PageSize(self):
        return self.__PageSize

    def get_current_user(self):
        user_id = self.get_secure_cookie("user")
        return user_id

    def on_finish(self):
        self.db.close_all()

    def write_error(self, status_code, **kwargs):
        import traceback
        exc_info = kwargs["exc_info"]
        trace_info = ''.join(["%s<br/>" % line for line in traceback.format_exception(*exc_info)])
        request_info = ''.join(
            ["<strong>%s</strong>: %s<br/>" % (k, self.request.__dict__[k]) for k in self.request.__dict__.keys()])
        error = exc_info[1]

        self.set_header('Content-Type', 'text/html')
        self.finish("""<html>
                         <title>%s</title>
                         <body>
                            <h2>Error</h2>
                            <p>%s</p>
                            <h2>Traceback</h2>
                            <p>%s</p>
                            <h2>Request Info</h2>
                            <p>%s</p>
                         </body>
                       </html>""" % (error, error,
                                     trace_info, request_info))


# class RESTfulHandler(BaseHandler):
#     RightEnable = True
#     @tornado.web.authenticated
#     def prepare(self):
#         self.CheckRith()
#
#     def CheckRith(self):
#         if self.RightEnable:
#             if self.get_current_user() == '1':
#                 return True
#             try:
#                 Rights = RightsCache.get("User{0}Right".format(self.get_current_user()))
#                 Rights = json.loads(Rights)
#                 righturl = [d.keys()[0] for d in Rights.values()[0]]
#                 if self.request.uri.split("/")[-2] or self.request.uri.split("/")[-1].split('?')[0] in righturl:
#                     for i in Rights.values()[0]:
#                         if i.get(self.request.uri.split("/")[-2],None) == None:
#                             continue
#                         else:
#                             if self.request.method.lower() in i.get(self.request.uri.split("/")[-2],None) or self.request.method.lower() in i.get(self.request.uri.split("/")[-1].split('?')[0],None):
#                                 return True
#                             else:
#                                 self.RightEnable = False
#                                 self.write({'errorMsg':'权限不足，不能进行该操作！','errorno':10000,'success':False})
#                 else:
#                     self.finish({'errorMsg': '权限不足，不能进行该操作！', 'errorno': 10002, 'success': False})
#             except Exception as e:
#                 self.finish({'errorMsg':'权限不足，不能进行该操作！','errorno':10001,'success':False})
#                 return False
