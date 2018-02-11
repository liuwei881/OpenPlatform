# -*- coding: utf-8 -*-
__author__ = 'liuwei'
__datetime__ = '16-3-9'

from lib.urlmap import urlmap
from lib.basehandler import BaseHandler
from tornado import web
from ldap3 import Connection, Server, ALL
import json


@urlmap(r'/login')
class LoginHandler(BaseHandler):
    @web.asynchronous
    def post(self):
        data = json.loads(self.request.body.decode("utf-8"))
        username = data['username']
        password = data['password']
        try:
            conn = Connection(Server('10.96.140.61', get_info=ALL), user='open\{}'.format(username),
                              password='{}'.format(password), auto_bind=True)
        except Exception as e:
            self.Result['info'] = u'登陆失败, 原因{}'.format(e)
            self.Result['status'] = 400
        else:
            if conn.bind():
                self.Result['info'] = u'登陆成功'
                self.Result['status'] = 200
                self.set_cookie('username', str(username), expires_days=0.5)
                self.set_secure_cookie('user', str(username), expires_days=0.5)
        self.finish(self.Result)


@urlmap(r'/logout')
class LogoutHandler(BaseHandler):
    def get(self):
        logid = self.get_cookie('logid')
        # if logid:
        #     # objLogLogin = self.db.query(UserLoginList).get(logid)
        #     objLogLogin.ExitTime = datetime.datetime.now()
        #     self.db.add(objLogLogin)
        #     self.db.commit()
        self.clear_cookie("user")
        self.clear_cookie("username")
        self.clear_cookie("logid")
        self.redirect('/#/login')
