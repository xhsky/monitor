#!/usr/bin/env python
# coding:utf8
# sky

from module import db, common, logger

class heartbeat(object):
    def __init__(self):
        self.__db_client=db.get_redis_conn()
        self.__heart_key="heartbeat"
    
    def heartbeat_info(self, heart_time):
        # 设置心跳信息

        value=self.election_value(heart_time)
        self.__db_client.setex(self.__key, heart_time, value)

    def obtain(self):
        # 获取集群中的ip, 并重新组织成heartbeat_ip的列表
        ip_list=self.__db_client.hgetall("host_soft_info").keys()
        ip_list=list(ip_list)

        for index, ip in enumerate(ip_list):
            ip_list[index]="_".join(["heartbeat", ip])

        heart_stat=self.__db_client.mget(ip_list)
        print(type(heart_stat))
        print(heart_stat)
        error_ips=[]
        election_list=[]

        for index, res in enumerate(heart_stat):
            if res is None:
                error_ip=ip_list[index].split("_")[1]
                error_ips.append(error_ip)
            else:
                election_list.append(res)
        return error_ips, res
    def election_value(self, heart_time):
        heart_time=int(heart_time)-1
        value=self.__db_client.incr("election", heart_time)
        return value
        
if __name__ == "__main__":
    pass
