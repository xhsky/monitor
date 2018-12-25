#!/usr/bin/env python
# coding:utf8
# sky

import yaml
from module import db, soft, logger, common

log=logger.logger()
def local_install(soft_name):
    with open("./conf/monitor.yml", "r") as config_file:
        res=yaml.load(config_file)
    install_dir=res["base_dir"]
    version=res["version"][soft_name]
    software_name="%s-%s.tar.xz" % (soft_name, version)

    sw=soft.install()
    sw.extra("./share/package/%s" % software_name, install_dir)

def local_control(soft_name, action):
    pass




def soft_install():
    with open("./conf/monitor.yml", "r") as config_file:
        res=yaml.load(config_file)

    ip=res["db"].get("ip")
    password=res["db"].get("password")
    port=res["db"].get("port")
    db_name=res["db"].get("db_name")
    local_db=res["database"]

    try: 
        db_client=db.redis_conn(ip, password, port, db_name)
        conn=db_client.connect()
        log.log("info", "安装程序已连接数据库")
    except Exception as e:
        log.log("critical", "安装程序无法连接数据库: %s" % e)

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
                if args["type"]=="install":
                    for soft_name in args["soft_name"]:
                        local_install(soft_name)
                elif args["type"]=="control":
                    local_control(args["soft_name"], args["action"])
                else:
                    pass


if __name__ == "__main__":
    pass










