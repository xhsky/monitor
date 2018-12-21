#!/usr/bin/env python
# coding:utf8
# sky

import gevent
from gevent import monkey
import time

import os, sys
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
from module import status

def interval_dump(dump, dump_type, dump_info):
    if type(dump_info).__name__ == 'dict':
        interval=dump_info["interval"]
        retain_num=int(dump_info["retain_hour"]*3600/interval)
    else:
        interval=dump_info

    if dump_type=="cpu_num":
        while True:
            dump.dump_cpu_num()
            time.sleep(interval)
    elif dump_type=="cpu_util":
        while True:
            dump.dump_cpu_util(interval, retain_num)
    elif dump_type=="mem_size":
        while True:
            dump.dump_mem_size()
            time.sleep(interval)
    elif dump_type=="mem_util":
        while True:
            dump.dump_mem_util(retain_num)
            time.sleep(interval)
    elif dump_type=="disk_info":
        while True:
            dump.dump_disk_info()
            time.sleep(interval)
    elif dump_type=="disk_util":
        while True:
            dump.dump_disk_util(retain_num)
            time.sleep(interval)
    elif dump_type=="network_io":
        while True:
            dump.dump_network_io(interval, retain_num)
    elif dump_type=="disk_io":
        while True:
            dump.dump_disk_io(interval, retain_num)
    elif dump_type=="users":
        while True:
            dump.dump_users()
            time.sleep(interval)
    else:
        pass


if __name__ == "__main__":
    monkey.patch_all()
    client=status.redis_conn("192.168.1.123", "b840fc02d524045429941cc15f59e41cb7be6c599")
    dump=status.dump_to_redis(client)

    args={
            "ip": "192.168.1.119", 
            "cpu_num": 5, 
            "cpu_util": {
                "interval": 2, 
                "retain_hour": 0.1
                }, 
            "mem_size": 5, 
            "mem_util": {
                "interval": 2, 
                "retain_hour": 0.1
                }, 
            "disk_info": 5, 
            "disk_util": {
                "interval": 2, 
                "retain_hour": 0.01
                }, 
            "network_io": {
                "interval": 2, 
                "retain_hour": 0.1
                }, 
            "disk_io": {
                "interval": 2, 
                "retain_hour": 0.1
                }, 
            "users": 5
            }

    gthread_list=[]
    for dump_type in args:
        gthread=gevent.spawn(interval_dump, dump, dump_type, args[dump_type])
        gthread_list.append(gthread)

    gevent.joinall(gthread_list)
