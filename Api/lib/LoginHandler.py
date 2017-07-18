# -*- coding: utf-8 -*-
__author__ = 'Hipeace86'
__datetime__ = '16-3-9'

from lib.urlmap import urlmap
from lib.basehandler import BaseHandler
from lib.tools import md5hash
from tornado import web
import datetime
# from lib.RedisCache import RightsCache
# from Right.Entity.UserModel import UserList
# from Right.Entity.UserRoleModel import UserRoleList
# from Right.Entity.RoleRightModel import RoleRightList
# from Right.Entity.MenuModel import MenuList
# from Right.Entity.UserLoginModel import UserLoginList
from sqlalchemy import desc,or_,and_
import json


@urlmap(r'/login')
class LoginHandler(BaseHandler):
    @web.asynchronous
    def get(self):
        account = self.get_argument('user', '')
        password = self.get_argument('password', '')
        if account == password:
            self.Result['info'] = u'登陆成功'
            self.Result['status'] = 200
            self.set_cookie('username', str(account), expires_days=0.5)
            self.set_secure_cookie('user', str(account), expires_days=0.5)
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
