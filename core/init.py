#!/usr/bin/env python
# coding:utf8
# sky

import os, sys
import yaml, json
from module import client, db, config

class init(object):
    def __init__(self, host_info_key):
        conf=config.config("./conf/monitor.yml")
        self.__host_info_key=host_info_key
        self.__res=conf.get_monitor_conf()
        self.__db_client=db.get_redis_conn()
        self.__host_client=client.client()

    def login(self):
        ip=self.__res["db"].get("ip")
        password=self.__res["db"].get("password")
        port=self.__res["db"].get("port")
        db_name=self.__res["db"].get("db_name")


        host_dict=self.__db_client.hgetall(self.__host_info_key)
        if host_dict is not None:
            stats=self.__host_client.password_conn(host_dict)
            if stats:
                host_client.gen_keys()
                host_client.key_conn(host_dict)
    def tarns(self, ):
        self.__host_client.transfer(self.__host_info_key,local_file, remote_path)

if __name__ == "__main__":
    pass
