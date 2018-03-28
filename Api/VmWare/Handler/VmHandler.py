# coding=utf-8

from lib.urlmap import urlmap
from lib.basehandler import BaseHandler
from tornado import web, gen
from VmWare.Entity.VmModel import VmwareList
from VmWare.Entity.IdModel import IdPool
import random
import json
from VmWare import tasks
from .functions import (get_datastores_info, get_datastores_max, get_ip)
from sqlalchemy import (desc, or_, and_)


@urlmap(r'/vms\/?([0-9]*)')
class VmsHandler(BaseHandler):
    @web.asynchronous
    def get(self, ident):
        """获取虚拟机信息"""
        username = self.get_cookie("username")
        page = int(self.get_argument('page', 1))
        searchKey = self.get_argument('searchKey', None)
        pagesize = int(self.get_argument('pagesize', self._PageSize))
        totalquery = self.db.query(VmwareList.VmwareId)
        VmwarelistObj = self.db.query(VmwareList)
        if searchKey:
            totalquery = totalquery.filter(
                or_(
                    VmwareList.VmwareName.like(
                        '%%%s%%' %
                        searchKey), VmwareList.Ip.like(
                        '%%%s%%' %
                        searchKey), VmwareList.HostName.like(
                        '%%%s%%' %
                        searchKey), VmwareList.WorkOrder.like(
                        '%%%s%%' %
                        searchKey)))
            VmwarelistObj = VmwarelistObj.filter(
                or_(
                    VmwareList.VmwareName.like(
                        '%%%s%%' %
                        searchKey), VmwareList.Ip.like(
                        '%%%s%%' %
                        searchKey), VmwareList.HostName.like(
                        '%%%s%%' %
                        searchKey)))
        self.Result['total'] = totalquery.count()
        serverTask = VmwarelistObj.order_by(
            desc(
                VmwareList.VmwareId)).limit(pagesize).offset(
            (page - 1) * pagesize).all()
        self.Result['rows'] = list(map(lambda obj: obj.toDict(), serverTask))
        self.Result['username'] = username
        self.finish(self.Result)

    @web.asynchronous
    def post(self, ident=0):
        """创建虚拟机"""
        data = json.loads(self.request.body.decode("utf-8"))
        objTask = VmwareList()
        objTask.WorkOrder = data['params'].get('WorkOrder', None)
        objTask.VmCpu = int(data['params'].get('VmCpu', None))
        objTask.VmMem = int(data['params'].get('VmMem', None)) * 1024
        objTask.TemplateName = data['params']['TemplateName'].get('name', None)
        objTask.DataCenter = data['params']['DataCenter'].get('name', None)
        objTask.Cluster = data['params']['Cluster'].get('name', None)
        objTask.ResourcePool = data['params']['ResourcePool'].get('name', None)
        objTask.CreatePerson = self.get_cookie("username")
        objTask.addressSegment = data['params'].get('addressSegment', None)
        objTask.Types = 'sys'
        objTask.HostStatus = 1
        number = int(data['params'].get('Number', None))
        datastore_list = get_datastores_info(
            'vmwin0466.open.com.cn',
            'open\\vc_auto',
            'openVC2018@@',
            443,
            objTask.DataCenter)
        network_dict = {'10.96.140': {'network': 'mdnet140', 'subnet': '255.255.255.0'},
                        '10.96.141': {'network': 'mdnet141', 'subnet': '255.255.255.0'},
                        '10.96.142': {'network': 'mdnet142', 'subnet': '255.255.255.0'},
                        '10.96.128': {'network': 'mdnet128', 'subnet': '255.255.255.0'},
                        '10.100.130': {'network': 'syqnet130', 'subnet': '255.255.254.0'},
                        '10.100.132': {'network': 'syqnet132', 'subnet': '255.255.254.0'},
                        '10.100.134': {'network': 'syqnet134', 'subnet': '255.255.254.0'},
                        '10.100.136': {'network': 'syqnet136', 'subnet': '255.255.254.0'},
                        '10.100.138': {'network': 'syqnet138', 'subnet': '255.255.255.0'},
                        '10.100.14': {'network': 'hltnet14', 'subnet': '255.255.254.0'},
                        '10.100.16': {'network': 'hltnet16', 'subnet': '255.255.254.0'},
                        '10.100.18': {'network': 'hltnet18', 'subnet': '255.255.254.0'},
                        '10.100.20': {'network': 'hltnet20', 'subnet': '255.255.255.0'}
                        }
        if number == 1:
            objTask.DataStore = random.choice(datastore_list)
            # ip = random.choice(ip_pool).Ip
            url = 'http://10.100.17.175:10001/ip/randomIp'
            for ip, network in network_dict.items():
                if ip in objTask.addressSegment:
                    objTask.NetworkName = network['network']
                    objTask.subnetMask = network['subnet']
            objTask.Ip = get_ip(url, objTask.addressSegment, objTask.subnetMask, objTask.Types)
            if '10.96' in objTask.Ip:
                id_pool = self.db.query(
                    IdPool.IdPool).filter(
                    IdPool.IdPool <= 4999)
                id = sorted(id_pool)[0][0]
                if id < 1000:
                    id = ''.join(['0', str(id)])
            elif '10.100.130' in objTask.Ip or '10.100.132' in objTask.Ip or '10.100.134' in objTask.Ip or '10.100.136' in objTask.Ip or '10.100.138' in objTask.Ip:
                id_pool = self.db.query(
                    IdPool.IdPool).filter(
                    and_(
                        IdPool.IdPool <= 6999,
                        IdPool.IdPool >= 5879))
                id = sorted(id_pool)[0][0]
            else:
                id_pool = self.db.query(
                    IdPool.IdPool).filter(
                    and_(
                        IdPool.IdPool <= 9999,
                        IdPool.IdPool >= 7637))
                id = sorted(id_pool)[0][0]
            if "centos" in objTask.TemplateName.lower() or "ubuntu" in objTask.TemplateName.lower(
            ) or 'mac' in objTask.TemplateName.lower():
                objTask.VmwareName = "_".join(
                    ["{}".format(id), "lin", "".join(objTask.Ip.split(".")[-2:])])
                objTask.HostName = "".join(["vmlin", "{}".format(id)])
            else:
                objTask.VmwareName = "_".join(
                    ["{}".format(id), "win", "".join(objTask.Ip.split(".")[-2:])])
                objTask.HostName = "".join(["vmwin", "{}".format(id)])
            tasks.create_vm.delay(
                'vmwin0466.open.com.cn', 'open\\vc_auto', 'openVC2018@@', 443,
                objTask.VmwareName, objTask.HostName, objTask.VmCpu,
                objTask.VmMem, objTask.TemplateName, objTask.Ip,
                objTask.DataCenter, objTask.Cluster, objTask.DataStore,
                objTask.ResourcePool, objTask.NetworkName)
            self.db.query(IdPool).filter(IdPool.IdPool == id).delete()
            self.db.add(objTask)
            self.db.commit()
        else:
            for i in range(number):
                objTask.DataStore = random.choice(datastore_list)
                url = 'http://10.100.17.175:10001/ip/randomIp'
                for ip, network in network_dict.items():
                    if ip in objTask.addressSegment:
                        objTask.NetworkName = network['network']
                        objTask.subnetMask = network['subnet']
                objTask.Ip = get_ip(url, objTask.addressSegment, objTask.subnetMask, objTask.Types)
                if '10.96' in objTask.Ip:
                    id_pool = self.db.query(
                        IdPool.IdPool).filter(
                        IdPool.IdPool <= 4999)
                    id = sorted(id_pool)[0][0]
                    if id < 1000:
                        id = ''.join(['0', str(id)])
                elif '10.100.130' in objTask.Ip or '10.100.132' in objTask.Ip or '10.100.134' in objTask.Ip or '10.100.136' in objTask.Ip or '10.100.138' in objTask.Ip:
                    id_pool = self.db.query(
                        IdPool.IdPool).filter(
                        and_(
                            IdPool.IdPool <= 6999,
                            IdPool.IdPool >= 5879))
                    id = sorted(id_pool)[0][0]
                else:
                    id_pool = self.db.query(
                        IdPool.IdPool).filter(
                        and_(
                            IdPool.IdPool <= 9999,
                            IdPool.IdPool >= 7637))
                    id = sorted(id_pool)[0][0]
                if "centos" in objTask.TemplateName.lower() or "ubuntu" in objTask.TemplateName.lower(
                ) or 'mac' in objTask.TemplateName.lower():
                    objTask.VmwareName = "_".join(
                        ["{}".format(id), "lin", "".join(objTask.Ip.split(".")[-2:])])
                    objTask.HostName = "".join(["vmlin", "{}".format(id)])
                else:
                    objTask.VmwareName = "_".join(
                        ["{}".format(id), "win", "".join(objTask.Ip.split(".")[-2:])])
                    objTask.HostName = "".join(["vmwin", "{}".format(id)])
                tasks.create_vm.delay(
                    'vmwin0466.open.com.cn',
                    'open\\vc_auto',
                    'openVC2018@@',
                    443,
                    objTask.VmwareName,
                    objTask.HostName,
                    objTask.VmCpu,
                    objTask.VmMem,
                    objTask.TemplateName,
                    objTask.Ip,
                    objTask.DataCenter,
                    objTask.Cluster,
                    objTask.DataStore,
                    objTask.ResourcePool,
                    objTask.NetworkName)
                pro = VmwareList(
                    WorkOrder=objTask.WorkOrder,
                    VmwareName=objTask.VmwareName,
                    HostName=objTask.HostName,
                    VmCpu=objTask.VmCpu,
                    VmMem=objTask.VmMem,
                    TemplateName=objTask.TemplateName,
                    Ip=objTask.Ip,
                    DataCenter=objTask.DataCenter,
                    Cluster=objTask.Cluster,
                    DataStore=objTask.DataStore,
                    ResourcePool=objTask.ResourcePool,
                    NetworkName=objTask.NetworkName,
                    CreatePerson=objTask.CreatePerson,
                    HostStatus=objTask.HostStatus
                )
                self.db.query(IdPool).filter(IdPool.IdPool == id).delete()
                self.db.add(pro)
                self.db.commit()
        self.Result['rows'] = 1
        self.Result['info'] = u'创建成功'
        self.finish(self.Result)

    @web.asynchronous
    def delete(self, ident):
        """删除虚拟机"""
        vm = self.db.query(VmwareList).filter(
            VmwareList.VmwareId == ident).first()
        ip = vm.Ip
        # ip_recycle = lambda x: sum([256 ** j * int(i) for j, i in enumerate(x.split('.')[::-1])])       # ip地址回收
        # pro = IpPool(Ip=ip_recycle(ip))
        # self.db.add(pro)
        tasks.del_vm.delay(
            'vmwin0466.open.com.cn',
            'open\\vc_auto',
            'openVC2018@@',
            443,
            ip)
        self.db.query(VmwareList).filter(VmwareList.VmwareId == ident).delete()
        self.db.commit()
        self.Result['info'] = u'删除虚拟机成功'
        self.finish(self.Result)


@urlmap(r'/vms/stop\/?([0-9]*)')
class StopHandler(BaseHandler):
    @web.asynchronous
    def get(self, ident):
        """关闭虚拟机"""
        vm = self.db.query(VmwareList).filter(
            VmwareList.VmwareId == ident).first()
        Ip = vm.Ip
        tasks.stop_vm.delay(
            'vmwin0466.open.com.cn',
            'open\\vc_auto',
            'openVC2018@@',
            443,
            Ip)
        self.Result['info'] = u'关闭虚拟机成功'
        self.finish(self.Result)


@urlmap(r'/vms/restart\/?([0-9]*)')
class RestartHandler(BaseHandler):
    @web.asynchronous
    def get(self, ident):
        """重启虚拟机"""
        vm = self.db.query(VmwareList).filter(
            VmwareList.VmwareId == ident).first()
        Name = vm.HostName
        if "vmwin" in Name:
            DnsName = ''.join([Name, ".open.com.cn"])
        else:
            DnsName = Name
        tasks.reboot_vm.delay(
            'vmwin0466.open.com.cn',
            'open\\vc_auto',
            'openVC2018@@',
            443,
            DnsName)
        self.Result['info'] = u'重启虚拟机成功'
        self.finish(self.Result)


@urlmap(r'/vms/migratevm\/?([0-9]*)')
class MigrateVmHandler(BaseHandler):
    @web.asynchronous
    def get(self, ident):
        """迁移虚拟机到其它存储"""
        vm = self.db.query(VmwareList).filter(
            VmwareList.VmwareId == ident).first()
        vmname = vm.VmwareName
        datacenter = vm.DataCenter
        DataStorage = get_datastores_max(
            'vmwin0466.open.com.cn',
            'open\\vc_auto',
            'openVC2018@@',
            443,
            datacenter)
        tasks.migration_vm.delay(
            'vmwin0466.open.com.cn',
            'open\\vc_auto',
            'openVC2018@@',
            443,
            DataStorage,
            vmname)
        self.db.query(VmwareList).filter(VmwareList.VmwareId == ident).update({
            'DataStore': DataStorage,
        })
        self.db.commit()
        self.Result['info'] = u'迁移虚拟机成功'
        self.finish(self.Result)
