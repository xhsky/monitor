#!/usr/bin/env python
# coding:utf8
# sky

from module import logger, soft, client, common, config, sysuser, define
from core import init
import yaml, sys, os

def install_redis(user):
    log.log("info", "本地安装redis数据库...")
    soft_name="redis"
    soft_install=soft.install(user, soft_name, base_dir)
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
    conf=config.config(conf_config)
    conf_res=conf.get_monitor_conf()

    # 系统用户
    system_user=conf_res["run_user"]
    system_password=conf_res["password"]

    # redis信息
    redis_port=conf_res["db"].get("port")
    redis_ip=conf_res["db"].get("ip")


    install_dir=conf_res["base_dir"]
    os.system("systemctl stop firewalld")
    os.system("systemctl disable firewalld")

    

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
    主机软件状态key
        host_soft_info  dict
          host_soft_info={
              "ip1": {
                  "tomcat": pid, 
                  "redis": pid 
                }, 
              "ip2": {
                  "tomcat": pid, 
                  "redis": pid 
                } 
            }
         
    """
    conn_host_info_key="conn_host_info"   
    if len(sys.argv)==2:
        action=sys.argv[1]
        client=client.client(redis_port)
        if action=="init":
            sysuser.useradd(system_user, system_password)
            # 安装本地redis
            install_redis(system_user)
            res=client.port_conn(redis_ip)
            if res==1:
                log.log("critical", "%s的%s端口无法连接, 请检查" % (redis_ip, redis_port))
                exit()
        elif action=="start":
            package="python37-monitor.tar.xz"
            local_file="%s/%s" %  (install_dir, package)
            remote_file="%s/%s" % (install_dir, package)
            remote_path=install_dir
            init=init.init()
            normal_ip_list=init.login(conn_host_info_key)
            init.tarns(local_file, remote_file, remote_path, normal_ip_list)
            init.start(normal_ip_list)
            start_command="%s/python/bin/python3 %s/monitor/main.py" % (conf_res["base_dir"],  conf_res["base_dir"])
            os.system(start_command)
        else:
            print("Usage: %s init|start\n" % sys.argv[0])
    else:
        print("Usage: %s init|start\n" % sys.argv[0])


