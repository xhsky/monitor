#!/usr/bin/env python
# coding:utf8
# sky

import gevent, yaml
from gevent import monkey
import time, json
import os, signal
from module import db, common, logger

from multiprocessing import Process

def mult_insert(args, name, ip):
    pid=os.getpid()
    print(ip, pid)
    db_client.hset(name, ip, pid)
    gthread_list=[]
    for dump_type in args:
        gthread=gevent.spawn(interval_dump, dump, dump_type, args[dump_type])
        gthread_list.append(gthread)

    gevent.joinall(gthread_list)

def interval_dump(dump, dump_type, dump_info):
    log=logger.logger()
    if type(dump_info).__name__ == 'dict':
        interval=dump_info["interval"]
        retain_num=int(dump_info["retain_hour"]*3600/interval)
    else:
        interval=dump_info

    if dump_type=="cpu_num":
        log.log("info", "开始记录%s资源" % dump_type)
        while True:
            log.log("debug", "正在记录%s资源" % dump_type)
            dump.dump_cpu_num()
            time.sleep(interval)

    elif dump_type=="cpu_util":
        log.log("info", "开始记录%s资源" % dump_type)
        while True:
            log.log("debug", "正在记录%s资源" % dump_type)
            dump.dump_cpu_util(interval, retain_num)

    elif dump_type=="mem_size":
        log.log("info", "开始记录%s资源" % dump_type)
        while True:
            log.log("debug", "正在记录%s资源" % dump_type)
            dump.dump_mem_size()
            time.sleep(interval)

    elif dump_type=="mem_util":
        log.log("info", "开始记录%s资源" % dump_type)
        while True:
            log.log("debug", "正在记录%s资源" % dump_type)
            dump.dump_mem_util(retain_num)
            time.sleep(interval)
    elif dump_type=="disk_info":
        log.log("info", "开始记录%s资源" % dump_type)
        while True:
            log.log("debug", "正在记录%s资源" % dump_type)
            dump.dump_disk_info()
            time.sleep(interval)
    elif dump_type=="disk_util":
        log.log("info", "开始记录%s资源" % dump_type)
        while True:
            log.log("debug", "正在记录%s资源" % dump_type)
            dump.dump_disk_util(retain_num)
            time.sleep(interval)
    elif dump_type=="network_io":
        log.log("info", "开始记录%s资源" % dump_type)
        while True:
            log.log("debug", "正在记录%s资源" % dump_type)
            dump.dump_network_io(interval, retain_num)
    elif dump_type=="disk_io":
        log.log("info", "开始记录%s资源" % dump_type)
        while True:
            log.log("debug", "正在记录%s资源" % dump_type)
            dump.dump_disk_io(interval, retain_num)
    elif dump_type=="users":
        log.log("info", "开始记录%s资源" % dump_type)
        while True:
            log.log("debug", "正在记录%s资源" % dump_type)
            dump.dump_users()
            time.sleep(interval)
    else:
        pass

def dump():
    monkey.patch_all()

    log=logger.logger()
    with open("./conf/monitor.yml", "r") as config_file:
        res=yaml.load(config_file)

    ip=res["db"].get("ip")
    password=res["db"].get("password")
    port=res["db"].get("port")
    db_name=res["db"].get("db_name")

    try: 
        db_client=db.redis_conn(ip, password, port, db_name)
        conn=db_client.connect()
        log.log("info", "监控程序已连接数据库")
    except Exception as e:
        log.log("critical", "监控无法连接数据库: %s" % e)

    dump=db.dump_to_redis(db_client)
    ip=common.host_ip()

    subs=db_client.subscribe("host_stat_info")  # host_stat_info 为订阅发布模式, 存储需要记录的资源类型
    """
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
    """
    log.log("info", "监控程序开始准备接收监控信息...")
    gthread_list=[]                                     # 定义记录资源的协程列表
    for i in subs.listen():
        if i["type"]=="message":
            args=json.loads(i["data"])
            if args["ip"]==ip:
                for i in gthread_list:                  # 杀掉原来的协程列表
                    gevent.kill(i)
                gthread_list=[]                         # 重置
                for dump_type in args:
                    gthread=gevent.spawn(interval_dump, dump, dump_type, args[dump_type])
                    gthread_list.append(gthread)
                #gevent.joinall(gthread_list)


if __name__ == "__main__":
    pass

