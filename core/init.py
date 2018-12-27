#!/usr/bin/env python
# coding:utf8
# sky

import os, sys
import yaml, json
from module import client, db, config

class init(object):
    def __init__(self, host_info_key):
        conf=config.config("./conf/monitor.yml")
        self.__res=conf.get_monitor_conf()
        self.__db_client=db.get_redis_conn()
        self.__host_client=client.client()
        self.__host_dict=self.__db_client.hgetall(host_info_key)

    def login(self):
        """
        校验端口连通和密码正确性, host_dict为 hostname:password 的字典, 
        """
        error_host_conn_key="host_error"    # 列表
        self.__host_client.gen_keys()

        if self.__host_dict is not None:
            for hostname in self.__host_dict.keys():
                stats=self.__host_client.password_conn(hostname, host_dict["hostname"])
                if stats=1:
                    self.__host_client.key_conn(hostname, host_dict["hostname"])
                    self.setenv(hostname)
                else:
                    self.__db_client.list_set(error_host_conn_key, stat)

    def setenv(self, hostname):
        """
            添加用户, dream权限, 关闭防火墙, 关闭selinux
        """
        user_name=self.__res["run_user"]
        user_password=self.__res["password"]
        commands="""
            useradd %s ; echo $s | passwd --stdin %s ; systemctl stop firewalld; systemctl disable firewalld
        """ % (user_name, user_password, user_name)

        self.__host_client.exec(hostname, commands)

    def tarns(self, local_file, remote_path):
        for hostname in self.__host_dict.keys():
            self.__host_client.transfer(hostname, local_file, remote_path)

if __name__ == "__main__":
    pass
