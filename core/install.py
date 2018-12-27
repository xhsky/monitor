#!/usr/bin/env python
# coding:utf8
# sky

import yaml
from module import db, soft, logger, common, config

class local_soft(object):
    def  __init__(self, soft_name):
        conf=config.config("./conf/monitor.yml")
        self.__log=logger.logger()
        self.__soft_name=soft_name
        self.__ip_soft_info_key="%s_soft_info" %  common.host_ip()
        self.__db_client=db.get_redis_conn()
        self.__res=conf.init_config()

    def local_install(self):
        install_dir=self.__res["base_dir"]
        user=self.__res["user"]
        version=self.__res["version"][soft_name]
        software_name="%s-%s.tar.xz" % (self.__soft_name, version)

        sw=soft.install(user, self.__soft_name, install_dir)
        sw.extra("%s/share/package/%s" % install_dir, software_name)
        sw.init()
        sw.init_data()
        self.__log.log("info", "%s已经安装" % self.__soft_name)
        
        db.redis_conn.hset(ip_soft_info_key, self.__soft_name, 0)

        """
            ip_soft_info={                          # 字典, 存储单台主机软件安装即启动情况
                "redis":3333,                       # 软件名:pid    pid为0则未启动
                "tomcat":4444, 
                "nginx": 0
            }
        """

    def local_control(self, action):
        install_dir=self.__res["base_dir"]
        user=self.__res["user"]
        sw=soft.install(user, self.__soft_name, install_dir)
        if action=="start":
            sw.set_env()
            pid=sw.start()
            self.__db_client.hset(self.__ip_soft_info_key, self.__soft_name, pid)
        elif action=="stop":
            sw.stop()
            self.__db_client.hset(self.__ip_soft_info_key, self.__soft_name, 0)

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
            args=json.load(i["data"])
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










