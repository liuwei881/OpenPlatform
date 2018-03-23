# coding=utf-8

from celery import Celery, task
import os
from pyVmomi import vim
from pyVim.connect import SmartConnect, Disconnect
import atexit
import requests
import ssl
import sys
import uuid
import time
from pyVmomi import vmodl

requests.packages.urllib3.disable_warnings()

# Disabling SSL certificate verification
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
context.verify_mode = ssl.CERT_NONE

#celery = Celery("tasks", broker="amqp://")
celery = Celery(
    "tasks",
    broker="amqp://admin:open@2018@rabbitmq.sysgroup.open.com.cn:5672//")
celery.conf.CELERY_RESULT_BACKEND = os.environ.get(
    'CELERY_RESULT_BACKEND', 'amqp')


celery.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_RESULT_SERIALIZER='json',
    CELERY_ROUTES={
        'tasks.create_vm': {'queue': 'vmware'},
        'tasks.del_vm': {'queue': 'vmware'},
        'tasks.stop_vm': {'queue': 'vmware'},
        'tasks.reboot_vm': {'queue': 'vmware'},
        'tasks.migration_vm': {'queue': 'vmware'},
    })


@celery.task(name='tasks.create_vm')
def create_vm(
        Host, User, Password, Port,
        VmwareName, HostName, VmCpu,
        VmMem, TemplateName, Ip,
        DataCenter, Cluster, DataStore,
        ResourcePool, NetworkName):
    """创建vmware虚拟机"""
    def wait_for_task(task):
        """ wait for a vCenter task to finish """
        task_done = False
        while not task_done:
            if task.info.state == 'success':
                return task.info.result
            if task.info.state == 'error':
                print("there was an error")
                task_done = True

    def get_obj(content, vimtype, name):
        """
        Return an object by name, if name is None the
        first found object is returned
        """
        obj = None
        container = content.viewManager.CreateContainerView(
            content.rootFolder, vimtype, True)
        for c in container.view:
            if name:
                if c.name == name:
                    obj = c
                    break
            else:
                obj = c
                break
        return obj

    def clone_vm(
            content, template, vm_name, si,
            datacenter_name, datastore_name,
            cluster_name, resource_pool, network_name, power_on=False):
        """
        Clone a VM from a template/VM, datacenter_name, vm_folder, datastore_name
        cluster_name, resource_pool, and power_on are all optional.
        """
        datacenter = get_obj(content, [vim.Datacenter], datacenter_name)
        destfolder = datacenter.vmFolder

        if datastore_name:
            datastore = get_obj(content, [vim.Datastore], datastore_name)
        else:
            datastore = get_obj(
                content, [vim.Datastore], template.datastore[0].info.name)

        cluster = get_obj(content, [vim.ClusterComputeResource], cluster_name)

        if resource_pool:
            resource_pool = get_obj(content, [vim.ResourcePool], resource_pool)
        else:
            resource_pool = cluster.resourcePool

        relospec = vim.vm.RelocateSpec()
        relospec.datastore = datastore
        relospec.pool = resource_pool

        clonespec = vim.vm.CloneSpec()
        clonespec.location = relospec
        clonespec.powerOn = power_on

        print("cloning VM...")

        task = template.Clone(folder=destfolder, name=vm_name, spec=clonespec)
        wait_for_task(task)

        vm = get_obj(content, [vim.VirtualMachine], vm_name)
        spec = vim.vm.ConfigSpec()
        spec.numCPUs = VmCpu
        spec.memoryMB = VmMem
        spec.name = VmwareName
        spec.uuid = str(uuid.uuid3(uuid.NAMESPACE_DNS, vm_name))

        device_change = []
        for device in vm.config.hardware.device:
            if isinstance(device, vim.vm.device.VirtualEthernetCard):
                nicspec = vim.vm.device.VirtualDeviceSpec()
                nicspec.operation = vim.vm.device.VirtualDeviceSpec.Operation.edit
                nicspec.device = device
                nicspec.device.wakeOnLanEnabled = True
                nicspec.device.backing = vim.vm.device.VirtualEthernetCard.NetworkBackingInfo()
                nicspec.device.backing.network = get_obj(
                    content, [vim.Network], network_name)
                nicspec.device.backing.deviceName = network_name
                nicspec.device.connectable = vim.vm.device.VirtualDevice.ConnectInfo()
                nicspec.device.connectable.startConnected = True
                nicspec.device.connectable.allowGuestControl = True
                device_change.append(nicspec)
                break
        spec.deviceChange = device_change
        print("reconfig task...")
        vm.ReconfigVM_Task(spec=spec)

        inputs = {'isDHCP': False,
                  'vm_ip': Ip,
                  'subnet': '255.255.255.0',
                  'gateway': '10.96.140.1',
                  'dns': ['10.96.140.61', '10.96.140.62'],
                  'domain': 'open.com.cn'
                  }
        gateway_dict = {'10.96.140':
                        {'gateway': '10.96.140.1', 'dns': ['10.96.140.61', '10.96.140.62'], 'subnet': '255.255.255.0'},
                        '10.96.141':
                            {'gateway': '10.96.141.1', 'dns': ['10.96.140.61', '10.96.140.62'], 'subnet': '255.255.255.0'},
                        '10.96.142':
                            {'gateway': '10.96.142.1', 'dns': ['10.96.140.61', '10.96.140.62'], 'subnet': '255.255.255.0'},
                        '10.96.128':
                            {'gateway': '10.96.128.1', 'dns': ['10.96.140.61', '10.96.140.62'], 'subnet': '255.255.255.0'},
                        '10.100.130':
                            {'gateway': '10.100.130.1', 'dns': ['10.100.132.13', '10.100.132.226'], 'subnet': '255.255.254.0'},
                        '10.100.132':
                            {'gateway': '10.100.132.1', 'dns': ['10.100.132.13', '10.100.132.226'], 'subnet': '255.255.254.0'},
                        '10.100.134':
                            {'gateway': '10.100.134.1', 'dns': ['10.100.132.13', '10.100.132.226'], 'subnet': '255.255.254.0'},
                        '10.100.136':
                            {'gateway': '10.100.136.1', 'dns': ['10.100.132.13', '10.100.132.226'], 'subnet': '255.255.254.0'},
                        '10.100.138':
                            {'gateway': '10.100.138.1', 'dns': ['10.100.132.13', '10.100.132.226'], 'subnet': '255.255.254.0'},
                        '10.100.14':
                            {'gateway': '10.100.14.1', 'dns': ['10.100.15.32', '10.100.15.212'], 'subnet': '255.255.254.0'},
                        '10.100.16':
                            {'gateway': '10.100.16.1', 'dns': ['10.100.15.32', '10.100.15.212'], 'subnet': '255.255.254.0'},
                        '10.100.18':
                            {'gateway': '10.100.18.1', 'dns': ['10.100.15.32', '10.100.15.212'], 'subnet': '255.255.254.0'},
                        '10.100.20':
                            {'gateway': '10.100.20.1', 'dns': ['10.100.15.32', '10.100.15.212'], 'subnet': '255.255.254.0'}
                        }
        for ip, gate in gateway_dict.items():
            if ip in Ip:
                inputs = {'isDHCP': False,
                          'vm_ip': Ip,
                          'subnet': gate['subnet'],
                          'gateway': gate['gateway'],
                          'dns': gate['dns'],
                          'domain': 'open.com.cn'
                          }

        if vm.runtime.powerState != 'poweredOff':
            print("WARNING:: Power off your VM before reconfigure")
            sys.exit()

        adaptermap = vim.vm.customization.AdapterMapping()
        globalip = vim.vm.customization.GlobalIPSettings()
        adaptermap.adapter = vim.vm.customization.IPSettings()

        isDHDCP = inputs['isDHCP']
        if not isDHDCP:
            """Static IP Configuration"""
            adaptermap.adapter.ip = vim.vm.customization.FixedIp()
            adaptermap.adapter.ip.ipAddress = inputs['vm_ip']
            adaptermap.adapter.subnetMask = inputs['subnet']
            adaptermap.adapter.gateway = inputs['gateway']
            globalip.dnsServerList = inputs['dns']
        else:
            """DHCP Configuration"""
            adaptermap.adapter.ip = vim.vm.customization.DhcpIpGenerator()
        adaptermap.adapter.dnsDomain = inputs['domain']
        # For Linux . For windows follow Sysprep
        if "centos" in vm.summary.config.guestFullName.lower() \
                or "ubuntu" in vm.summary.config.guestFullName.lower() \
                or "mac" in vm.summary.config.guestFullName.lower():
            ident = vim.vm.customization.LinuxPrep(
                domain=inputs['domain'],
                hostName=vim.vm.customization.FixedName(
                    name=vm_name))
        else:
            ident = vim.vm.customization.Sysprep()
            # 不自动登录
            ident.guiUnattended = vim.vm.customization.GuiUnattended(
                autoLogon=False)
            # windows用户名和计算机名，组织名称
            ident.userData = vim.vm.customization.UserData()
            ident.userData.fullName = VmwareName
            ident.userData.orgName = "Open"
            ident.userData.computerName = vim.vm.customization.FixedName()
            ident.userData.computerName.name = vm_name
            # windows加入域
            ident.identification = vim.vm.customization.Identification()
            ident.identification.joinDomain = "open.com.cn"
            ident.identification.domainAdmin = "domainreg"
            ident.identification.domainAdminPassword = vim.vm.customization.Password()
            ident.identification.domainAdminPassword.plainText = True
            ident.identification.domainAdminPassword.value = "OpenReg2017"

        customspec = vim.vm.customization.Specification()
        # For only one adapter
        customspec.identity = ident
        customspec.nicSettingMap = [adaptermap]
        customspec.globalIPSettings = globalip
        print("Reconfiguring VM Networks . . .")
        task = vm.Customize(spec=customspec)
        wait_for_task(task)
        vm.PowerOn()

    si = SmartConnect(
        host=Host,
        user=User,
        pwd=Password,
        port=Port, sslContext=context)
    # disconnect this thing
    atexit.register(Disconnect, si)
    content = si.RetrieveContent()
    template = get_obj(content, [vim.VirtualMachine], TemplateName)

    if template:
        clone_vm(
            content, template, HostName, si,
            DataCenter, DataStore, Cluster,
            ResourcePool, NetworkName)
    else:
        print("template not found")
    return "create vmware ok"


@task(name='tasks.del_vm')
def del_vm(Host, User, Password, Port, Ip):
    """删除虚拟机"""
    def wait_for_tasks(service_instance, tasks):
        """Given the service instance si and tasks, it returns after all the tasks are complete"""
        property_collector = service_instance.content.propertyCollector
        task_list = [str(task) for task in tasks]
        # Create filter
        obj_specs = [vmodl.query.PropertyCollector.ObjectSpec(obj=task)
                     for task in tasks]
        property_spec = vmodl.query.PropertyCollector.PropertySpec(
            type=vim.Task, pathSet=[], all=True)
        filter_spec = vmodl.query.PropertyCollector.FilterSpec()
        filter_spec.objectSet = obj_specs
        filter_spec.propSet = [property_spec]
        pcfilter = property_collector.CreateFilter(filter_spec, True)
        try:
            version, state = None, None
            # Loop looking for updates till the state moves to a completed
            # state.
            while len(task_list):
                update = property_collector.WaitForUpdates(version)
                for filter_set in update.filterSet:
                    for obj_set in filter_set.objectSet:
                        task = obj_set.obj
                        for change in obj_set.changeSet:
                            if change.name == 'info':
                                state = change.val.state
                            elif change.name == 'info.state':
                                state = change.val
                            else:
                                continue
                            if not str(task) in task_list:
                                continue
                            if state == vim.TaskInfo.State.success:
                                # Remove task from taskList
                                task_list.remove(str(task))
                            elif state == vim.TaskInfo.State.error:
                                raise task.info.error
                # Move to next version
                version = update.version
        finally:
            if pcfilter:
                pcfilter.Destroy()

    si = SmartConnect(
        host=Host,
        user=User,
        pwd=Password,
        port=Port, sslContext=context)
    # disconnect this thing
    atexit.register(Disconnect, si)
    if not si:
        raise SystemExit(
            "Unable to connect to host with supplied credentials.")
    VM = si.content.searchIndex.FindByIp(None, Ip, True)

    if VM is None:
        raise SystemExit(
            "Unable to locate VirtualMachine. Arguments given: "
            "ip - {0}".format(Ip)
        )
    print("Found: {0}".format(VM.name))
    print("The current powerState is: {0}".format(VM.runtime.powerState))
    if format(VM.runtime.powerState) == "poweredOn":
        print("Attempting to power off {0}".format(VM.name))
        TASK = VM.PowerOffVM_Task()
        wait_for_tasks(si, [TASK])
        print("{0}".format(TASK.info.state))
    print("Destroying VM from vSphere.")
    TASK = VM.Destroy_Task()
    wait_for_tasks(si, [TASK])
    print("Done.")
    return "del vmware ok"


@task(name='tasks.stop_vm')
def stop_vm(Host, User, Password, Port, Ip):
    """关闭虚拟机"""
    def wait_for_tasks(service_instance, tasks):
        """Given the service instance si and tasks, it returns after all the tasks are complete"""
        property_collector = service_instance.content.propertyCollector
        task_list = [str(task) for task in tasks]
        # Create filter
        obj_specs = [vmodl.query.PropertyCollector.ObjectSpec(obj=task)
                     for task in tasks]
        property_spec = vmodl.query.PropertyCollector.PropertySpec(
            type=vim.Task, pathSet=[], all=True)
        filter_spec = vmodl.query.PropertyCollector.FilterSpec()
        filter_spec.objectSet = obj_specs
        filter_spec.propSet = [property_spec]
        pcfilter = property_collector.CreateFilter(filter_spec, True)
        try:
            version, state = None, None
            # Loop looking for updates till the state moves to a completed
            # state.
            while len(task_list):
                update = property_collector.WaitForUpdates(version)
                for filter_set in update.filterSet:
                    for obj_set in filter_set.objectSet:
                        task = obj_set.obj
                        for change in obj_set.changeSet:
                            if change.name == 'info':
                                state = change.val.state
                            elif change.name == 'info.state':
                                state = change.val
                            else:
                                continue
                            if not str(task) in task_list:
                                continue
                            if state == vim.TaskInfo.State.success:
                                # Remove task from taskList
                                task_list.remove(str(task))
                            elif state == vim.TaskInfo.State.error:
                                raise task.info.error
                # Move to next version
                version = update.version
        finally:
            if pcfilter:
                pcfilter.Destroy()
    si = SmartConnect(host=Host,
                      user=User,
                      pwd=Password,
                      port=Port, sslContext=context)
    atexit.register(Disconnect, si)
    if not si:
        raise SystemExit("Unable to connect to host with supplied info.")
    VM = si.content.searchIndex.FindByIp(None, Ip, True)
    if VM is None:
        raise SystemExit("Unable to locate VirtualMachine.")
    print("Found: {0}".format(VM.name))
    print("The current powerState is: {0}".format(VM.runtime.powerState))
    TASK = VM.PowerOffVM_Task()
    wait_for_tasks(si, [TASK])
    return "shutdown vmware {0} ok.".format(VM.name)


@task(name='tasks.reboot_vm')
def reboot_vm(Host, User, Password, Port, DnsName):
    """重启虚拟机"""
    def wait_for_tasks(service_instance, tasks):
        """Given the service instance si and tasks, it returns after all the tasks are complete"""
        property_collector = service_instance.content.propertyCollector
        task_list = [str(task) for task in tasks]
        # Create filter
        obj_specs = [vmodl.query.PropertyCollector.ObjectSpec(obj=task)
                     for task in tasks]
        property_spec = vmodl.query.PropertyCollector.PropertySpec(
            type=vim.Task, pathSet=[], all=True)
        filter_spec = vmodl.query.PropertyCollector.FilterSpec()
        filter_spec.objectSet = obj_specs
        filter_spec.propSet = [property_spec]
        pcfilter = property_collector.CreateFilter(filter_spec, True)
        try:
            version, state = None, None
            # Loop looking for updates till the state moves to a completed
            # state.
            while len(task_list):
                update = property_collector.WaitForUpdates(version)
                for filter_set in update.filterSet:
                    for obj_set in filter_set.objectSet:
                        task = obj_set.obj
                        for change in obj_set.changeSet:
                            if change.name == 'info':
                                state = change.val.state
                            elif change.name == 'info.state':
                                state = change.val
                            else:
                                continue
                            if not str(task) in task_list:
                                continue
                            if state == vim.TaskInfo.State.success:
                                # Remove task from taskList
                                task_list.remove(str(task))
                            elif state == vim.TaskInfo.State.error:
                                raise task.info.error
                # Move to next version
                version = update.version
        finally:
            if pcfilter:
                pcfilter.Destroy()
    si = SmartConnect(host=Host,
                      user=User,
                      pwd=Password,
                      port=Port, sslContext=context)
    atexit.register(Disconnect, si)
    if not si:
        raise SystemExit("Unable to connect to host with supplied info.")
    VM = si.content.searchIndex.FindByDnsName(None, DnsName, True)
    if VM is None:
        raise SystemExit("Unable to locate VirtualMachine.")
    print("Found: {0}".format(VM.name))
    print("The current powerState is: {0}".format(VM.runtime.powerState))
    if VM.runtime.powerState == 'poweredOn':
        TASK = VM.ResetVM_Task()
        wait_for_tasks(si, [TASK])
    else:
        VM.PowerOn()
    return "reboot vmware {0} ok.".format(VM.name)


@celery.task(name='tasks.migration_vm')
def migration_vm(Host, User, Password, Port, DataStorage, VmName):
    """迁移虚拟机存储"""
    def get_obj(content, vimtype, name):
        """Get the vsphere object associated with a given text name"""
        obj = None
        container = content.viewManager.CreateContainerView(
            content.rootFolder, vimtype, True)
        for c in container.view:
            if c.name == name:
                obj = c
                break
        return obj

    def wait_for_task(task, actionName='job', hideResult=False):
        """Waits and provides updates on a vSphere task"""
        while task.info.state == vim.TaskInfo.State.running:
            time.sleep(2)

        if task.info.state == vim.TaskInfo.State.success:
            if task.info.result is not None and not hideResult:
                out = '%s completed successfully, result: %s' % (
                    actionName, task.info.result)
                print(out)
            else:
                out = '%s completed successfully.' % actionName
                print(out)
        else:
            out = '%s did not complete successfully: %s' % (
                actionName, task.info.error)
            print(out)
            raise task.info.error
        return task.info.result

    si = SmartConnect(
        host=Host,
        user=User,
        pwd=Password,
        port=Port,
        sslContext=context)
    atexit.register(Disconnect, si)
    content = si.RetrieveContent()
    vm = get_obj(content, [vim.VirtualMachine], VmName)
    if vm.runtime.powerState != 'poweredOn':
        print("WARNING:: Migration is only for Powered On VMs")
        sys.exit()
    vm_relocate_spec = vim.vm.RelocateSpec()
    datastore = get_obj(content, [vim.Datastore], DataStorage)
    vm_relocate_spec.datastore = datastore
    task = vm.Relocate(spec=vm_relocate_spec)
    print("migarate finish")
    wait_for_task(task, si)
    return "migarate is ok"