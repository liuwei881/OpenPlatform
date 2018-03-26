# coding=utf-8

import subprocess
import pymysql
import multiprocessing


def ping_status(ip_list):
    '''检查服务器ping状态,{2: 'online', 3: 'offline'}'''
    cmd_status = {}
    for ip in ip_list:
        if subprocess.call(
            'ping -c 1 -W 1 %s > /dev/null' %
                ip, shell=True) == 0:
            cmd_status[ip] = 2
        else:
            cmd_status[ip] = 3
    return cmd_status


def get_ip():
    '''获取服务器ip列表'''
    db = pymysql.connect("127.0.0.1", "root", "123456", "virmath")
    cursor = db.cursor()
    sql = 'select fs_ip from bk_vmware_list;'
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        ip_list = [row[0] for row in results]
    except Exception as e:
        print("error")
    db.close()
    return ip_list


if __name__ == "__main__":
    ip_list = get_ip()

    if len(ip_list) > 30:
        process_number = 30
    else:
        process_number = len(ip_list)
    pool = multiprocessing.Pool(processes=process_number)
    pool.apply_async(ping_status, (ip_list,))
    pool.close()
    pool.join()

    host_dic = ping_status(ip_list)

    db = pymysql.connect("127.0.0.1", "root", "123456", "virmath")
    cursor = db.cursor()
    for k, v in host_dic.items():
        sql = "update bk_vmware_list set fi_hoststatus={0} where fs_ip='{1}'".format(
            v, k)
        try:
            cursor.execute(sql)
            db.commit()
        except Exception as e:
            print(e)
    db.close()
