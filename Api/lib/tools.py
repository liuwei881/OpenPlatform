#coding=utf-8

import hashlib


def md5hash(data):
    '''计算密码md5'''
    hash_md5 = hashlib.md5(data)
    return hash_md5.hexdigest()
