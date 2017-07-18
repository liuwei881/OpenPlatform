#coding=utf-8

import time
import atexit
import json
import requests
import ssl
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim


requests.packages.urllib3.disable_warnings()

# Disabling SSL certificate verification
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
context.verify_mode = ssl.CERT_NONE


def curDatetime():
    """生成时间格式"""
    return time.strftime('%Y-%m-%d %X', time.localtime())


def getStatusId(ident):
    """虚拟机状态"""
    statusDIct = {1: 'pending', 2: 'online', 3: 'down'}
    if ident and ident in statusDIct.keys():
        return statusDIct[ident]
    else:
        return ident


def sizeof_fmt(num):
    """返回可读性强的硬盘大小"""
    for item in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, item)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')


def get_obj(content, vimtype, name=None):
    """Return an object by name, if name is None the first found object is returned"""
    obj = None
    container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
    for c in container.view:
        if name:
            if c.name == name:
                obj = c
                break
        else:
            obj = c
            break
    return obj

def get_datastores_info(host, user, pwd, port, datacenter):
    """获取存储信息"""
    si = SmartConnect(host=host, user=user, pwd=pwd, port=port, sslContext=context)
    atexit.register(Disconnect, si)
    content = si.RetrieveContent()
    datacenter = get_obj(content, [vim.Datacenter], datacenter)
    ds_obj_list = datacenter.datastore
    datastores_info = {}
    for ds in ds_obj_list:
        summary = ds.summary
        ds_capacity = summary.capacity
        ds_freespace = summary.freeSpace
        datastores_info[summary.name] = {}
        datastores_info[summary.name]["capacity"] = sizeof_fmt(ds_capacity)
        datastores_info[summary.name]["freespace"] = sizeof_fmt(ds_freespace)
    #template_disk = get_obj(content, [vim.VirtualMachine], templatename)
    space = slice(0, -2)
    #datastores_list = [k for k, v in datastores_info.items() if v["freespace"].endswith("GB") and int(float(v["freespace"][space])) > int(float(sizeof_fmt(template_disk.summary.storage.uncommitted)[space]))*2.5 or v["freespace"].endswith("TB")]
    datastores_list = [k for k, v in datastores_info.items() if v["freespace"].endswith("GB") and int(float(v["freespace"][space])) > 400 or v["freespace"].endswith("TB")]
    return datastores_list


def get_datastores_max(Host, User, Pwd, Port, datacenter):
    """获取剩余空间最大的存储"""
    si = SmartConnect(host=Host, user=User, pwd=Pwd, port=Port, sslContext=context)
    atexit.register(Disconnect, si)
    content = si.RetrieveContent()
    datacenter = get_obj(content, [vim.Datacenter], datacenter)
    ds_obj_list = datacenter.datastore
    datastores_max = {ds.summary.name: sizeof_fmt(ds.summary.freeSpace) for ds in ds_obj_list}
    datastores_max_new = {}
    for k, v in datastores_max.items():
        s = slice(0, -2)
        if v.endswith('TB'):
            v = float(v[s])*1024
            datastores_max_new[k] = v
        elif v.endswith('GB'):
            v = float(v[s])
            datastores_max_new[k] = v
    max_datastore = max((v, k) for (k, v) in datastores_max_new.items())[1]
    return max_datastore