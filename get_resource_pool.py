# coding=utf-8


from pyVmomi import vim, vmodl
from pyVim.connect import SmartConnect, Disconnect
import atexit
import requests
import ssl
requests.packages.urllib3.disable_warnings()

# Disabling SSL certificate verification
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
context.verify_mode = ssl.CERT_NONE


def list_obj(content, vimtype):
    container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
    return container.view


def get_obj(content, vimtype, name):
    obj = None
    container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
    for c in container.view:
        if c.name == name:
            obj = c
            break
    return obj


def get_resource_pool(vcenter_server, vcenter_username, vcenter_password, port, resource_pool_name=''):
    """获取所有的资源池"""
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    context.verify_mode = ssl.CERT_NONE
    service_instance = SmartConnect(
            host=vcenter_server,
            user=vcenter_username,
            pwd=vcenter_password,
            port=port,
            sslContext=context)
    content = service_instance.RetrieveContent()
    atexit.register(Disconnect, service_instance)
    resource_pool_list = []
    if resource_pool_name == '':
        listOBJ = list_obj(content, [vim.ResourcePool])
    else:
        listOBJ = get_obj(content, [vim.ResourcePool], resource_pool_name)
    for each in listOBJ:
        resource_pool_list.append(each.name)
    return resource_pool_list


if __name__ == '__main__':
    host = 'vmwin0466.open.com.cn'
    user = 'open\\vc_auto'
    pwd = 'openVC2018@@'
    port = 443
    print(get_resource_pool(host, user, pwd, port))

