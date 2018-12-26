#!/usr/bin/env python
# coding:utf8
# sky

import psutil

class soft_status(object):
    def __init__(self, pid):
        self.__pid=pid

    def pid_exist(self):
        pids=psutil.pids()
        return self.__pid in pids

if __name__ == "__main__":
    pass
