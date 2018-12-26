#!/usr/bin/env python
# coding:utf8
# sky

from module import logger, soft, client, common
from core import init
import yaml, sys, os

def install_redis(user):
    log.log("info", "本地安装redis数据库")
    soft_name="redis"
    soft_install=soft.install(user, soft_name, "./redis" )
    soft_install.init()
    soft_install.set_env()
    soft_install.start()


if __name__ == "__main__":
    base_dir=common.base_dir(__file__)
    os.chdir(base_dir)

    # 日志
    logger_config="%s/conf/logger.yml" %  base_dir
    log=logger.logger(logger_config)

    # 获取配置
    conf_config="%s/conf/monitor.yml" % base_dir
    with open(conf_config, "r", encoding="utf8") as config_file:
        conf=yaml.load(config_file)

    install_dir=conf["base_dir"]
    user=conf["run_user"]

    redis_port=conf["db"].get("port")
    redis_ip=conf["db"].get("ip")
    redis_db=conf["db"].get("db_name")
    redis_password=conf["db"].get("password")
    if redis_ip=="localhost" or redis_ip=="127.0.0.1":
        log.log("critical", "%s中db选项下ip必须为域名或实际IP" % conf_config)
        exit()

    """
    "mult_main.py init|start"
    """

    """
    获取主机信息key
        conn_host_info 为redis中的dict, 存储hostname:password的字典
        conn_host_info={
            "192.168.1.11":"password", 
            "192.168.1.12":"password",
            "192.168.1.13":"password", 
            "192.168.1.14":"password" 
        }
    """
    conn_host_info_key="conn_host_info"   
    if sys.argv==2:
        action=sys.argv[1]
        client=client.client(redis_port)
        if action=="init":
            # 安装本地redis
            install_redis(user)

            db_client=db.redis_conn(ip, password, port, db_name)
        conn=db_client.connect()
            res=client.port_conn(redis_ip)
            if res==1:
                log.log("critical", "%s的%s端口无法连接, 请检查" % (redis_ip, redis_port))
                exit()
        elif action=="start":
            # 
            init=init.init(conn_host_info_key)
            init.login()
            init.tarns()
        else:
            print("Usage: %s init|start\n" % sys.argv[0])
    else:
        print("Usage: %s init|start\n" % sys.argv[0])
