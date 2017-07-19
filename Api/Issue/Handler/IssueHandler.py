#coding=utf-8

from lib.urlmap import urlmap
from lib.basehandler import BaseHandler
from tornado import web,gen
from Issue.Entity.IssueModel import IssueServer
import json
from sqlalchemy import desc,or_,and_,engine
from Issue import tasks

@urlmap(r'/issue\/?([0-9]*)')
class NgHandler(BaseHandler):
    @web.asynchronous
    def get(self, ident):
        """获取发布信息"""
        username = self.get_cookie("username")
        page = int(self.get_argument('page', 1))
        searchKey = self.get_argument('searchKey', None)
        pagesize = int(self.get_argument('pagesize', self._PageSize))
        totalquery = self.db.query(IssueServer.Id)
        NgIssueObj = self.db.query(IssueServer)
        if searchKey:
            totalquery = totalquery.filter(or_(IssueServer.DomainName.like('%%%s%%' % searchKey),IssueServer.HealthExam.like('%%%s%%' % searchKey),IssueServer.Port.like('%%%s%%' % searchKey)))
            NgIssueObj = NgIssueObj.filter(or_(IssueServer.DomainName.like('%%%s%%' % searchKey),IssueServer.HealthExam.like('%%%s%%' % searchKey),IssueServer.Port.like('%%%s%%' % searchKey)))
        self.Result['total'] = totalquery.count()
        serverTask = NgIssueObj.order_by(desc(IssueServer.Id)).limit(pagesize).offset((page - 1) * pagesize).all()
        self.Result['rows'] = list(map(lambda obj: obj.toDict(), serverTask))
        self.Result['username'] = username
        self.finish(self.Result)

    @web.asynchronous
    def post(self, ident=0):
        """创建nginx及consul"""
        data = json.loads(self.request.body.decode("utf-8"))
        objTask = IssueServer()
        domainname = data['params'].get('DomainName', None)
        objTask.DomainName = domainname + ".openkf.cn"
        objTask.HealthExam = data['params'].get('HealthExam', None)
        objTask.Port = int(data['params'].get('Port', None))
        objTask.Publisher = self.get_cookie("username")
        self.db.add(objTask)
        self.db.commit()
        tasks.nginx_issue.delay(domainname, objTask.Port, objTask.HealthExam)
        self.Result['rows'] = 1
        self.Result['info'] = u'创建成功'
        self.finish(self.Result)

    @web.asynchronous
    def delete(self, ident):
        """删除nginx及consul"""
        # vm = self.db.query(VmwareList).filter(VmwareList.VmwareId==ident).first()
        # ip = vm.Ip
        # ip_recycle = lambda x: sum([256 ** j * int(i) for j, i in enumerate(x.split('.')[::-1])])       # ip地址回收
        # pro = IpPool(Ip=ip_recycle(ip))
        # self.db.add(pro)
        # tasks.del_vm.delay('10.96.140.157', 'autovm', '1qaz!QAZ', 443, ip)
        # self.db.query(VmwareList).filter(VmwareList.VmwareId == ident).delete()
        # self.db.commit()
        # self.Result['info'] = u'删除虚拟机成功'
        # self.finish(self.Result)
        pass
