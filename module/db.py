#!/usr/bin/env python
# coding:utf8
# sky

import psutil, redis
import time, json, socket
from module import logger, config, common

class redis_conn(object):
    def __init__(self, host, password, port=6379, db=0):
        self.__pool=redis.ConnectionPool(host=host, password=password, port=port, db=db, encoding='utf-8', decode_responses=True)
        self.log=logger.logger()

    def connect(self):
        self.__conn=redis.Redis(connection_pool=self.__pool)

    def str_set(self, key, values):
        temp=json.dumps(values)
        self.__conn.set(key, temp)
    def incr(self, key, second):
        self.__conn.incr(key)
        self.__conn.expire(key, second)
    
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
    def setex(self, key, second, value):
        temp=json.dumps(value)
        self.__conn.setex(key, second, temp)
    def mget(self, keys):
        self.__conn.mget(keys)


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

