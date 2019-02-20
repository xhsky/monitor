#!/usr/bin/env python
# coding:utf8
# sky

import gevent, yaml
from gevent import monkey
import time, json
from module import db, common, logger, stats, define

class store_to_redis(object):
    def __init__(self, redis_object):
        self.__log=logger.logger()
        self.__obj=redis_object
        self.__obj.connect()
        self.__ip=common.host_ip()
        self.__host_stats=stats.host_status()

    def store_cpu_num(self):
        cpu_num=self.__host_stats.cpu_num()
        self.__obj.str_set('%s_cpu_num' % self.__ip, cpu_num) 

    def store_cpu_util(self,interval, retain_num):
        cpu_util=self.__host_stats.cpu_util(interval)
        self.__obj.stat_list_set("%s_cpu_util" % self.__ip, cpu_util, retain_num)

    def store_mem_size(self):
        mem_size=self.__host_stats.mem_size()
        self.__obj.str_set('%s_mem_size' % self.__ip, mem_size)

    def store_mem_util(self, retain_num=1):
        mem_util=self.__host_stats.mem_util()
        self.__obj.stat_list_set('%s_mem_util' % self.__ip, mem_util, retain_num)

    def store_disk_info(self):
        disk_info=self.__host_stats.disk_info()
        self.__obj.str_set('%s_disk_info' % self.__ip,disk_info)

    def store_disk_util(self, retain_num=1):
        disk_util=self.__host_stats.disk_util()
        self.__obj.stat_list_set("%s_disk_util" % self.__ip, disk_util, retain_num)

    def store_network_io(self, interval=5, retain_num=1):
        network_io=self.__host_stats.network_io(interval)
        self.__obj.stat_list_set("%s_network_io" % self.__ip, network_io, retain_num)

    def store_disk_io(self, interval=5, retain_num=1):
        disk_io=self.__host_stats.disk_io(interval)
        self.__obj.stat_list_set("%s_disk_io" % self.__ip, disk_io, retain_num)

    def store_users(self):
        users=self.__host_stats.users()
        self.__obj.str_set("%s_users" % self.__ip, users) 

    def store_soft(self, soft_name, pid, interval, retain_time):
        retain_num=retain_time*3600//interval
        soft_info=stats.soft_status(pid)
        while True:
            soft_info_dict=soft_info.info()
            soft_stat_info_key="%s_%s_%s" % (self.__ip, soft_name, define.soft_stat_info_key)
            self.__obj.stat_list_set(soft_stat_info_key, soft_info_dict, retain_num)
            time.sleep(interval)

    def host_stats_store(self, resource_type, resource_info):
        if type(resource_info).__name__ == 'dict':
            interval=resource_info["interval"]
            retain_num=int(resource_info["retain_hour"]*3600/interval)
        else:
            interval=resource_info

        if resource_type=="cpu_num":
            self.__log.log("info", "开始记录%s资源" % resource_type)
            while True:
                self.__log.log("debug", "正在记录%s资源" % resource_type)
                self.store_cpu_num()
                time.sleep(interval)

        elif resource_type=="cpu_util":
            self.__log.log("info", "开始记录%s资源" % resource_type)
            while True:
                self.__log.log("debug", "正在记录%s资源" % resource_type)
                self.store_cpu_util(interval, retain_num)

        elif resource_type=="mem_size":
            self.__log.log("info", "开始记录%s资源" % resource_type)
            while True:
                self.__log.log("debug", "正在记录%s资源" % resource_type)
                self.store_mem_size()
                time.sleep(interval)

        elif resource_type=="mem_util":
            self.__log.log("info", "开始记录%s资源" % resource_type)
            while True:
                self.__log.log("debug", "正在记录%s资源" % resource_type)
                self.store_mem_util(retain_num)
                time.sleep(interval)
        elif resource_type=="disk_info":
            self.__log.log("info", "开始记录%s资源" % resource_type)
            while True:
                self.__log.log("debug", "正在记录%s资源" % resource_type)
                self.store_disk_info()
                time.sleep(interval)
        elif resource_type=="disk_util":
            self.__log.log("info", "开始记录%s资源" % resource_type)
            while True:
                self.__log.log("debug", "正在记录%s资源" % resource_type)
                self.store_disk_util(retain_num)
                time.sleep(interval)
        elif resource_type=="network_io":
            self.__log.log("info", "开始记录%s资源" % resource_type)
            while True:
                self.__log.log("debug", "正在记录%s资源" % resource_type)
                self.store_network_io(interval, retain_num)
        elif resource_type=="disk_io":
            self.__log.log("info", "开始记录%s资源" % resource_type)
            while True:
                self.__log.log("debug", "正在记录%s资源" % resource_type)
                self.store_disk_io(interval, retain_num)
        elif resource_type=="users":
            self.__log.log("info", "开始记录%s资源" % resource_type)
            while True:
                self.__log.log("debug", "正在记录%s资源" % resource_type)
                self.store_users()
                time.sleep(interval)
        else:
            pass

    def soft_stats_store(self, name, interval, retain_time):
        soft_name=self.__obj.hget(define.host_soft_info_key, self.__ip)
        if soft_name is not None:
            soft_name_dict=json.loads(soft_name)
            if name in soft_name_dict:
                pid=int(soft_name_dict[name])
                if pid!=0:
                    self.store_soft(name, pid, interval, retain_time)
                else:
                    self.__log.log("error", "%s主机上的%s未启动" % (self.__ip, name))
            else:
                self.__log.log("error", "%s未在%s主机上安装" % (name, self.__ip))
        else:
            self.__log.log("error", "%s主机不在集群中" % self.__ip)
        
def store():
    monkey.patch_all()

    log=logger.logger()
    db_client=db.get_redis_conn()

    store_obj=store_to_redis(db_client)
    ip=common.host_ip()

    subs=db_client.subscribe(define.stat_info_key)                         # host_stat_info 为订阅发布模式, 存储需要记录的资源类型
    log.log("info", "监控程序开始准备接收监控信息...")
    gthread_host_list=[]                                     # 定义记录主机资源的协程列表
    gthread_soft_list=[]                                     # 定义记录软件资源的协程列表
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
                        for resource_type in args:
                            gthread=gevent.spawn(store_obj.host_stats_store, resource_type, args[resource_type])
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
                        soft_names_dict=args["soft_name"]
                        for soft in soft_names_dict:
                            gthread=gevent.spawn(store_obj.soft_stats_store, soft, soft_names_dict[soft][0], soft_names_dict[soft][1])
                            gthread_soft_list.append(gthread)
                    elif args["action"]=="stop":
                        log.log("info", "软件资源记录已关闭")
                        
if __name__ == "__main__":
    print("main pid", os.getpid())
    store()

