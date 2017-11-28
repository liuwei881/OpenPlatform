#coding=utf-8


def getStatusId(ident):
    """健康检查状态"""
    statusDIct = {1: 'online', 2: 'down'}
    if ident and ident in statusDIct.keys():
        return statusDIct[ident]
    else:
        return ident