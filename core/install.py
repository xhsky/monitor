#!/usr/bin/env python
# coding:utf8
# sky

import yaml, json
from module import db, soft, logger, common, config

class local_soft(object):
    def  __init__(self, soft_name):
        conf=config.config("./conf/monitor.yml")
        self.__log=logger.logger()
        self.__soft_name=soft_name
        self.__db_client=db.get_redis_conn()
        self.__res=conf.get_monitor_conf()

    def local_install(self):
        # 获取安装包路径
        install_dir=self.__res["base_dir"]
        user=self.__res["run_user"]
        version=self.__res["version"][self.__soft_name]
        software_name="%s-%s.tar.gz" % (self.__soft_name, version)
        # 获取已安装软件信息
        host_soft_info_key="host_soft_info"
        key=common.host_ip()
        soft_info=self.__db_client.hget(host_soft_info_key, key)
        soft_info_dict=json.loads(soft_info)
        if self.__soft_name in soft_info_dict:
            self.__log.log("error", "%s已在%s上安装" % (self.__soft_name, key))
        else:
            self.__log.log("info", "%s开始安装..." % self.__soft_name)
            sw=soft.install(user, self.__soft_name, install_dir)
            stats=sw.extra("%s/monitor/share/package/%s" % (install_dir, software_name))
            if stats==0:
                sw.init()
                sw.init_data()
                self.__log.log("info", "%s已经安装" % self.__soft_name)
              
                # 加入安装软件信息
                soft_info_dict[self.__soft_name]="0"
                soft_info=json.dumps(soft_info_dict)
                self.__db_client.hset(host_soft_info_key, key, soft_info)

    def local_control(self, action):
        install_dir=self.__res["base_dir"]
        user=self.__res["run_user"]
        sw=soft.install(user, self.__soft_name, install_dir)
        # 获取已安装软件信息
        host_soft_info_key="host_soft_info"
        key=common.host_ip()
        soft_info=self.__db_client.hget(host_soft_info_key, key)
        soft_info_dict=json.loads(soft_info)

        pid=soft_info_dict[self.__soft_name]
        if action=="start":
            if self.__soft_name in soft_info_dict and pid=="0":
                sw.set_env()
                pid=sw.start()
                if pid!=0:
                    soft_info_dict[self.__soft_name]=pid
                    soft_info=json.dumps(soft_info_dict)
                    self.__db_client.hset(host_soft_info_key, key, soft_info)
###############################
                    print(soft_info)
                else:
                    self.__log.log("error", "无法启动, 请查看%s状态" % self.__soft_name)
            else:
                self.__log.log("error", "%s 是启动状态" % self.__soft_name)
                
        elif action=="stop":
            if self.__soft_name in soft_info_dict and pid!="0":
                res=sw.stop(pid)
                if res==0:
                    soft_info_dict[self.__soft_name]="0"
                    soft_info=json.dumps(soft_info_dict)
                    self.__db_client.hset(host_soft_info_key, key, soft_info)
            else:
                self.__log.log("error", "%s 未启动" % self.__soft_name)
                
        else:
            self.__log.log("error", "action: %s" % action)

def soft_install():
    log=logger.logger()
    db_client=db.get_redis_conn()
    ip=common.host_ip()

    soft_install_info_key="soft_install_info"   # 主机安装软件信息key, 以订阅发布方式
    """
        前端传递数据格式样例
        安装:
        args={
            "ip": "192.168.1.131", 
            "type": "install"
            "soft_name": ["redis", "tomcat", "mysql", "nginx"]
            }
        }
        控制
        args={
            "ip": "192.168.1.131", 
            "type": "control", 
            "soft_name": "redis", 
            "action": "start|stop"
            }
        }
    """

    log.log("info", "安装程序开始准备接收安装信息...")
    subs=db_client.subscribe(soft_install_info_key)
    for i in subs.listen():
        if i["type"]=="message":
            args=json.loads(i["data"])
            if args["ip"]==ip:
                # 安装
                if args["type"]=="install":
                    for soft_name in args["soft_name"]:
                        local_soft_obj=local_soft(soft_name)
                        local_soft_obj.local_install()
                # 控制
                elif args["type"]=="control":
                    local_soft_obj=local_soft(args["soft_name"])
                    local_soft_obj.local_control(args["action"])
                # 其它
                else:
                    pass


if __name__ == "__main__":
    pass


