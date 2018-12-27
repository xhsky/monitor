#!/usr/bin/env python
# coding:utf8
# sky

import os
from module import logger

def useradd(user, password):
    log=logger.logger()
    res=os.system("useradd %s" % user)
    if res==0 or res==2304:
        log.log("info", "%s用户添加成功" % user)
        res=os.system("echo %s | passwd --stdin %s" % (password, user))
        if res==0:
            log.log("info", "%s用户设置密码成功" % user)

    else:
        print(res)
        log.log("error", "%s用户无法添加" % user)


if __name__ == "__main__":
    pass
