#!/usr/bin/env python
# coding:utf8
# sky

import gevent, yaml
from gevent import monkey
import time, json, os
from module import db, common, logger, stats, define

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

def soft_stat_dump(name, interval=2):
    log=logger.logger()
    db_client=db.get_redis_conn()
    ip=common.host_ip()
    soft_name=db_client.hget(define.host_soft_info_key, ip)
    if soft_name is not None:
        soft_name_dict=json.loads(soft_name)
        if name in soft_name_dict:
            pid=int(soft_name_dict[name])
            if pid!=0:
                soft_info=stats.soft_status(pid)
                while True:
                    soft_info_dict=soft_info.info()
                    soft_stat_info_key="%s_%s_%s" % (ip, name, define.soft_stat_info_key)
                    db_client.stat_list_set(soft_stat_info_key, soft_info_dict, 3000)
                    time.sleep(interval)
            else:
                log.log("error", "%s主机上的%s未启动" % (ip, name))
        else:
            log.log("error", "%s未在%s主机上安装" % (name, ip))
    else:
        log.log("error", "%s主机不在集群中" % ip)
        

    

def dump():
    monkey.patch_all()

    log=logger.logger()
    db_client=db.get_redis_conn()

    dump=db.dump_to_redis(db_client)
    ip=common.host_ip()

    subs=db_client.subscribe(define.stat_info_key)                         # host_stat_info 为订阅发布模式, 存储需要记录的资源类型
    log.log("info", "监控程序开始准备接收监控信息...")
    gthread_host_list=[]                                     # 定义记录资源的协程列表
    gthread_soft_list=[]                                     # 定义记录资源的协程列表
    for i in subs.listen():
        if i["type"]=="message":
            args=json.loads(i["data"])
            if args["ip"]==ip:
                if args["type"]=="host":
                    for i in gthread_host_list:                  # 杀掉原来的协程列表
                        gevent.kill(i)
                    gthread_host_list=[]                         # 重置
                    if args["action"]=="start":
                        log.log("info", "主机资源记录开启")
                        for dump_type in args:
                            gthread=gevent.spawn(interval_dump, dump, dump_type, args[dump_type])
                            gthread_host_list.append(gthread)
                        #gevent.joinall(gthread_list)
                    elif args["action"]=="stop":
                        log.log("info", "主机资源记录已关闭")
                elif args["type"]=="soft":
                    for i in gthread_soft_list:                  # 杀掉原来的协程列表
                        gevent.kill(i)
                    gthread_soft_list=[]                         # 重置
                    if args["action"]=="start":
                        log.log("info", "软件资源记录开启")
                        for soft in args["soft_name"]:
                            gthread=gevent.spawn(soft_stat_dump, soft)
                        gthread_soft_list.append(gthread)
                    elif args["action"]=="stop":
                        log.log("info", "软件资源记录已关闭")
                        
if __name__ == "__main__":
    pass

