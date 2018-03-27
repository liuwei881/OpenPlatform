# coding=utf-8
from sqlalchemy import Column, Integer, String, Text, DateTime
from lib.Route import BaseModel
from VmWare.Handler.functions import getStatusId
import datetime


class VmwareList(BaseModel):
    """
    镜像显示列表
    """
    __tablename__ = 'bk_vmware_list'

    VmwareId = Column('fi_id', Integer, primary_key=True)
    WorkOrder = Column('fs_work_order', String(50))
    VmwareName = Column('fs_vmwarename', String(40))
    HostName = Column('fs_hostname', String(20))
    VmCpu = Column('fi_cpu', Integer)
    VmMem = Column('fi_mem', Integer)
    TemplateName = Column('fs_templatename', String(50))
    Ip = Column('fs_ip', String(15))
    DataCenter = Column('fs_datacenter', String(50))
    Cluster = Column('fs_cluster', String(50))
    DataStore = Column('fs_datastore', String(50))
    ResourcePool = Column('fs_resourcepool', String(50))
    NetworkName = Column('fs_networkname', String(50))
    Types = Column('fs_types', String(50))
    CreatePerson = Column('fs_create_person', String(50))
    HostStatus = Column('fi_hoststatus', Integer)
    CreateTime = Column(
        'ft_create_time',
        DateTime,
        default=datetime.datetime.now())

    def toDict(self):
        return {
            'VmwareId': self.VmwareId,  # id
            'WorkOrder': self.WorkOrder,    # 工单编号
            'VmwareName': self.VmwareName,  # 虚拟机名称
            'HostName': self.HostName,  # 虚拟机hostname
            'VmCpu': self.VmCpu,
            'VmMem': self.VmMem,
            'TemplateName': self.TemplateName,  # 模版名称
            'Ip': self.Ip,
            'DataCenter': self.DataCenter,  # 数据中心
            'Cluster': self.Cluster,  # 集群
            'DataStore': self.DataStore,  # 存储
            'ResourcePool': self.ResourcePool,  # 资源池
            'NetworkName': self.NetworkName,  # 网络名称
            'Types': self.Types,  # 使用类型组, 网络组net, 系统组sys
            'CreatePerson': self.CreatePerson,  # 创建人
            'HostStatus': getStatusId(self.HostStatus),  # 状态
            'StatusNum': self.HostStatus,
            'CreateTime': self.CreateTime.strftime('%Y-%m-%d %H:%M:%S') if self.CreateTime else ''
        }