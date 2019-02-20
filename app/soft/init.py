#!/usr/bin/env python
# coding:utf8
# sky

import json
from module import client, db, config, logger, common, define

class init(object):
    def __init__(self):
        self.__log=logger.logger()
        conf=config.config("./conf/monitor.yml")
        self.__res=conf.get_monitor_conf()
        self.__db_client=db.get_redis_conn()
        self.__host_client=client.client()

    def passwd_free(self, host_info_key):
        host_dict=self.__db_client.hgetall(host_info_key)
        """
        校验端口连通和密码正确性, host_dict为 hostname:password 的字典, 
        """
        self.__host_client.gen_keys()       # 生成秘钥 

        normal_ip_list=[]
        exists_host_dict=self.__db_client.hgetall("host_soft_info")
        for hostname in host_dict.keys():
          if hostname not in exists_host_dict.keys():
                stats=self.__host_client.password_conn(hostname, host_dict[hostname])
                if stats==1:
                    self.__host_client.key_conn(hostname, host_dict[hostname])
                    self.setenv(hostname)
                    # 将正常ip写入redis
                    soft_info_dict={}
                    soft_info=json.dumps(soft_info_dict)
                    self.__db_client.hset(define.host_soft_info_key, hostname, soft_info)
                    normal_ip_list.append(hostname)
                else:
                    # 将有问题ip写入redis
                    self.__db_client.list_set(define.error_host_conn_key, stats)
          else:
            self.__log.log("error", "%s主机已存在, 不要重复输入" % hostname)

        return normal_ip_list

    def setenv(self, hostname):
        """
            添加用户, dream权限, 关闭防火墙, 关闭selinux
        """
        user_name=self.__res["run_user"]
        user_password=self.__res["password"]
        commands="""
            useradd %s ; echo %s | passwd --stdin %s ; systemctl stop firewalld; systemctl disable firewalld
        """ % (user_name, user_password, user_name)

        self.__host_client.exec(hostname, commands)
        self.__log.log("info", "%s完成系统环境初始化" % hostname)

    def tarns(self, local_file, remote_file, remote_path, ip_list):
        for hostname in ip_list:
            if hostname==common.host_ip():
                self.__log.log("error", "本机安装包传输忽略")
            else:
              self.__host_client.transfer(hostname, local_file, remote_file, remote_path)
        else:
            self.__log.log("info", "各主机传输完成")

    def start(self, ip_list):
        start_command="%s/python/bin/python3 %s/monitor/main.py start" % (self.__res["base_dir"], self.__res["base_dir"])
        for hostname in ip_list:
            self.__host_client.exec(hostname, start_command)
            self.__log.log("info", "%s主机监控程序已启动" % hostname)
    def restart(self, ip_list):
        start_command="%s/python/bin/python3 %s/monitor/main.py restart" % (self.__res["base_dir"], self.__res["base_dir"])
        for hostname in ip_list:
            self.__host_client.exec(hostname, start_command)
            self.__log.log("info", "%s主机监控程序已启动" % hostname)
            
if __name__ == "__main__":
    pass
