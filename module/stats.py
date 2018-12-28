#!/usr/bin/env python
# coding:utf8
# sky

import psutil, time

class soft_status(object):
    def __init__(self, pid):
        self.__pid=pid

    def pid_exist(self):
        res=psutil.pid_exists(self.__pid)
        return res

    def info(self):
        process=psutil.Process(self.__pid)
        info_list=["pid", "create_time", "connections", "num_threads", "cpu_percent", "memory_percent", "username"]
        info_dict=process.as_dict(attrs=info_list)
        info_dict["time"]=time.time()
        info_dict["connections"]=len(info_dict["connections"])
        return info_dict

class host_status(object):
    def __init__(self):
        pass

if __name__ == "__main__":
    pass
