#coding=utf-8

import json
import pycurl
from io import BytesIO
import requests

requests.packages.urllib3.disable_warnings()
url = 'https://10.96.140.63:8888'


def api_login():
    url = 'https://10.96.140.63:8888/login'
    ch = pycurl.Curl()
    ch.setopt(ch.URL, url)
    info = BytesIO()
    ch.setopt(ch.WRITEFUNCTION, info.write)
    ch.setopt(ch.POST, True)
    ch.setopt(ch.SSL_VERIFYPEER, 0)
    ch.setopt(ch.SSL_VERIFYHOST, 2)
    ch.setopt(ch.HTTPHEADER, ['Accept: application/x-yaml'])
    ch.setopt(ch.POSTFIELDS, 'username=saltapi&password=liuwei1201abc&eauth=pam')
    ch.setopt(ch.HEADER,False)
    ch.perform()
    html = info.getvalue().decode('utf-8')
    token = html.split("\n")[-3].replace("\n", '')
    token = token.split(' ')[3]
    info.close()
    ch.close()
    return token


def get_result(cmd, arg, token=api_login(), tgt='*', tgt_type='glob'):
    data = json.dumps([{"client": "local", "tgt": tgt, "fun": cmd, "arg": arg, 'tgt_type': tgt_type}])
    header = {"Content-Type":"application/json", "Accept": "application/x-yaml", "X-Auth-Token": "{0}".format(token)}
    request = requests.post(url=url, data=data, headers=header, verify=False)
    return request.text


if __name__ == "__main__":
    print(get_result("cmd.run", "ls", tgt="rancher_group", tgt_type="nodegroup"))
