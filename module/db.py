#!/usr/bin/env python
# coding:utf8
# sky

import psutil, redis
import time, json, socket
from module import logger, config
#import sqlite3

class redis_conn(object):
    def __init__(self, host, password, port=6379, db=0):
        self.__pool=redis.ConnectionPool(host=host, password=password, port=port, db=db, encoding='utf-8', decode_responses=True)
        self.log=logger.logger()

    def connect(self):
        self.__conn=redis.Redis(connection_pool=self.__pool)

    def str_set(self, key, values):
        temp=json.dumps(values)
        self.__conn.set(key, temp)
    
    def str_get(self, key):
        temp=self.__conn.get(key)
        data=json.loads(temp)
        return data

    def stat_list_set(self, key, values, retain_num):
        temp=json.dumps(values)
        self.__conn.lpush(key, temp)
        self.__conn.ltrim(key, 0, retain_num)

    def list_set(self, key, values):
        temp=json.dumps(values)
        self.__conn.lpush(key, temp)

    def list_get(self, key):
        temp=self.__conn.rpop(key)
        if temp is None:
            self.log.log("warn","前台未向数据库写入数据")
        else:
            data=json.loads(temp)
            return data

    def publish(self, channel, message):
        temp=json.dumps(message)
        self.__conn.publish(channel, temp)

    def subscribe(self, channel):
        ps=self.__conn.pubsub()
        ps.subscribe(channel)
        return ps

    def hget(self, name, key):
        return self.__conn.hget(name, key)
    def hgetall(self, name):
        return self.__conn.hgetall(name)

    def hset(self, name, key, value):
        self.__conn.hset(name, key, value)
    def hmset(self, name, dict_key):
        self.__conn.hmset(name, dict_key)

    def brpop(self, key):
        self.__conn.brpop(key, timeout=0)

    def __del__(self):
        pass        

class sqlite_conn(object):
    def __init__(self, database):
        self.__conn=sqlite3.connect(database)
        self.__cursor=self.__conn.cursor()

    def create(self, sql):
        self.__cursor.execute(sql)

    def update(self, sql, value):
        self.__cursor.execute(sql, value)

    def insert(self, sql, data):
        self.__cursor.executemany(sq1, data)

    def fetchall(self, sql):
        self.__cursor.fetchall(sql)

    def commit(self):
        self.__conn.commit()

    def __del__(self):
        self.__cursor.close()
        self.__conn.close()

class soft_status(object):
    def __init__(self):
        pass

class dump_to_redis(object):
    def __init__(self, redis_object):
        self.__obj=redis_object
        self.__obj.connect()

        try:
            s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            self.__ip = s.getsockname()[0]
        finally:
            s.close()
    def dump_cpu_num(self):
        cpu_num={'time':time.time()}
        cpu_num['cpu_physical_core']=psutil.cpu_count(logical=False)
        cpu_num['cpu_logic_core']=psutil.cpu_count()
        self.__obj.str_set('%s_cpu_num' % self.__ip, cpu_num) 

    def dump_cpu_util(self,interval, retain_num):
        cpu_percent=psutil.cpu_percent(interval)
        cpu_util={
                "time": time.time(), 
                "cpu_percent": cpu_percent
                }
        self.__obj.stat_list_set("%s_cpu_util" % self.__ip, cpu_util, retain_num)

    def dump_mem_size(self):
        mem_size={'time':time.time()}
        mem_size['total']=psutil.virtual_memory()[0]
        mem_size['swap_total']=psutil.swap_memory()[0]
        self.__obj.str_set('%s_mem_size' % self.__ip, mem_size)

    def dump_mem_util(self, retain_num=1):
        mem_util={'time':time.time()}
        temp1=psutil.virtual_memory()
        temp2=psutil.swap_memory()
        
        mem_util={
                "time": time.time(), 
                "available": temp1[1], 
                "percent": temp1[2], 
                "used": temp1[3], 
                "free": temp1[4], 
                "buffers": temp1[7],
                "cache": temp1[8], 
                "shared": temp1[9], 
                "swap_used": temp2[1], 
                "swap_used": temp2[2], 
                "swap_percent": temp2[3]
                }
        self.__obj.stat_list_set('%s_mem_util' % self.__ip, mem_util, retain_num)

    def dump_disk_info(self):
        disk_info={'time':time.time()}
        temp=psutil.disk_partitions()
        for i, disk in enumerate(temp, start=1):
            disk_info[disk[1]]={
                    "device": disk[0], 
                    "fstype": disk[2], 
                    "total": psutil.disk_usage(disk[1])[0]
                    }
        self.__obj.str_set('%s_disk_info' % self.__ip,disk_info)

    def dump_disk_util(self, retain_num=1):
        disk_util={'time':time.time()}
        temp=psutil.disk_partitions()
        for disk in temp:
            single_disk_util=psutil.disk_usage(disk[1])
            disk_util[disk[1]]={
                    "used": single_disk_util[1], 
                    "free": single_disk_util[2], 
                    "percent": single_disk_util[3]
                    }
        self.__obj.stat_list_set("%s_disk_util" % self.__ip, disk_util, retain_num)

    def dump_network_io(self, interval=5, retain_num=1):
        start_io=psutil.net_io_counters()
        time.sleep(interval)
        end_io=psutil.net_io_counters()
        network_io={"time":time.time()}
        network_io["bytes_sent"]=int((end_io[0]-start_io[0])/interval)
        network_io["bytes_recv"]=int((end_io[1]-start_io[1])/interval)
        self.__obj.stat_list_set("%s_network_io" % self.__ip, network_io, retain_num)

    def dump_disk_io(self, interval=5, retain_num=1):
        start_io=psutil.disk_io_counters()
        time.sleep(interval)
        end_io=psutil.disk_io_counters()
        disk_io={"time":time.time()}
        disk_io["read_bytes"]=int((end_io[2]-start_io[2])/interval)
        disk_io["write_bytes"]=int((end_io[3]-start_io[3])/interval)
        self.__obj.stat_list_set("%s_disk_io" % self.__ip, disk_io, retain_num)

    def dump_users(self):
        users={"time":time.time()}
        temp=psutil.users()
        for i, user in enumerate(temp, start=1):
            users["user%s" % i]={
                    "name": user[0], 
                    "terminal": user[1], 
                    "host": user[2], 
                    "started": user[3]
                    }
        self.__obj.str_set("%s_users" % self.__ip, users) 

def get_redis_conn():
    log=logger.logger()
    conf=config.config("./conf/monitor.yml")
    conf_res=conf.get_monitor_conf()

    redis_port=conf_res["db"].get("port")
    redis_ip=conf_res["db"].get("ip")
    redis_db=conf_res["db"].get("db_name")
    redis_password=conf_res["db"].get("password")
    if redis_ip=="localhost" or redis_ip=="127.0.0.1":
        log.log("critical", "%s中db选项下ip必须为域名或实际IP" % conf_config)
        exit()

    try:
        db_client=redis_conn(redis_ip, redis_password, redis_port, redis_db)
        conn=db_client.connect()
        log.log("info", "已连接数据库开始操作")
        return db_client
    except Exception as e:
        log.log("critical", "无法连接数据库: %s" % e)


if __name__ == "__main__":
    ip="192.168.1.119"
    red_client=redis_conn("192.168.1.123","b840fc02d524045429941cc15f59e41cb7be6c599")

    a=dump_to_redis(red_client)
    a.dump_cpu_num()
    a.dump_cpu_util(2)
    a.dump_mem_size()
    a.dump_mem_util()
    a.dump_disk_info()
    a.dump_disk_util()
    a.dump_network_io(2)
    a.dump_disk_io(2)
    a.dump_users()

