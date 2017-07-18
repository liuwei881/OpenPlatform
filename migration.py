#coding=utf-8

'''
Copyright 2013-2014 Reubenur Rahman
All Rights Reserved
@author: reuben.13@gmail.com
'''

from pyVmomi import vim
from pyVim.connect import SmartConnect, Disconnect
import atexit
import requests
import ssl
import sys, time
from pyVmomi import vmodl

requests.packages.urllib3.disable_warnings()

# Disabling SSL certificate verification
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
context.verify_mode = ssl.CERT_NONE

inputs = {'vcenter_ip': '15.22.10.11',
          'vcenter_password': 'Password123',
          'vcenter_user': 'Administrator',
          'vm_name': 'ubuntu12',
          'destination_host': '15.22.11.9'
          }


def get_obj(content, vimtype, name):
	"""
	Get the vsphere object associated with a given text name
	"""
	obj = None
	container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
	for c in container.view:
		if c.name == name:
			obj = c
			break
	return obj

def wait_for_task(task, actionName='job', hideResult=False):
	"""
	Waits and provides updates on a vSphere task
	"""
	while task.info.state == vim.TaskInfo.State.running:
		time.sleep(2)

	if task.info.state == vim.TaskInfo.State.success:
		if task.info.result is not None and not hideResult:
			out = '%s completed successfully, result: %s' % (actionName, task.info.result)
			print(out)
		else:
			out = '%s completed successfully.' % actionName
			print(out)
	else:
		out = '%s did not complete successfully: %s' % (actionName, task.info.error)
		print(out)
		raise task.info.error
	return task.info.result

def main():
	try:
		si = SmartConnect(host=inputs['vcenter_ip'], port=443, user=inputs['vcenter_user'], pwd=inputs['vcenter_password'], sslContext=context)
		atexit.register(Disconnect, si)
		print("Connected to VCENTER SERVER !")
		content = si.RetrieveContent()
		vm = get_obj(content, [vim.VirtualMachine], inputs['vm_name'])
		if vm.runtime.powerState != 'poweredOn':
				print("WARNING:: Migration is only for Powered On VMs")
				sys.exit()

		vm_relocate_spec = vim.vm.RelocateSpec()
		datastore = get_obj(content, [vim.Datastore], "U114localStorage")
		vm_relocate_spec.datastore = datastore
		task = vm.Relocate(spec=vm_relocate_spec)
		print("migarate finish")
		wait_for_task(task, si)

	except vmodl.MethodFault as e:
		print("Caught vmodl fault: %s" % e.msg)
		return 1
	except Exception as e:
		print("Caught exception: %s" % str(e))
		return 1

# Start program
if __name__ == "__main__":
	main()