#!/usr/bin/env python
# coding:utf8
# sky

import gevent, yaml
from gevent import monkey
import time, socket, json
import os, sys
base_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
from module import db

from multiprocessing import Process
import signal

def host_ip():
    try:
        s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        return ip
    finally:
        s.close()

def mult_insert(args, name, ip):
    pid=os.getpid()
    print(ip, pid)
    db_client.hset(name, ip, pid)
    gthread_list=[]
    for dump_type in args:
        gthread=gevent.spawn(interval_dump, dump, dump_type, args[dump_type])
        gthread_list.append(gthread)

    print("insert 函数开始")
    gevent.joinall(gthread_list)
    print("insert 函数结束")

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

    with open("../conf/monitor.yml", "r") as config_file:
        res=yaml.load(config_file)

    ip=res["db"].get("ip")
    password=res["db"].get("password")
    port=res["db"].get("port")
    db_name=res["db"].get("db_name")

    db_client=db.redis_conn(ip, password, port, db_name)
    conn=db_client.connect()

    dump=db.dump_to_redis(db_client)
    ip=host_ip()
    stat_pid="stat_pid"                     # 记录每台主机执行插入主机状态的进程pid

    subs=db_client.subscribe("host_stat_info")
    for i in subs.listen():
        if i["type"]=="message":
            args=json.loads(i["data"])
            if args["ip"]==ip:
                pid=db_client.hget(stat_pid, ip)
                if pid is not None:
                    try:
                        res=os.kill(int(pid), signal.SIGKILL)
                    except ProcessLookupError as e:
                        pass
                p=Process(target=mult_insert, args=(args, stat_pid, ip))
                p.start()




