#!/usr/bin/env python
# coding:utf8
# sky

from module import logger, common, db, stats
from core import install,stat_dump 
import gevent
from gevent import monkey
import yaml, psutil

import os, time

def Install():
    log.log("info", "安装程序启动")
    install.soft_install()

def Status():
    log.log("info", "监控程序启动")
    stat_dump.dump()

if __name__ == "__main__":
    monkey.patch_all() 

    base_dir=common.base_dir(__file__)
    os.chdir(base_dir)

    # 日志
    logger_config="%s/conf/logger.yml" %  base_dir
    log=logger.logger(logger_config)

    # 获取配置
    conf_config="%s/conf/monitor.yml" % base_dir
    with open(conf_config, "r", encoding="utf8") as config_file:
        conf=yaml.load(config_file)
    pid_file=conf["pid"]
    db_name=conf["database"]
    
    """
    # pid
    db_name_path="%s/data/%s" % (base_dir, db_name)
    db_client=db.sqlite_conn(db_name_path)
    sql="create table if not exists process_id(ip char(15) primary key, pid int)"
    db_client.create(sql)

    ip=common.host_ip()
    pid=os.getpid()
    #sql="insert into process_id values(?,?) on conflict(ip) do update set pid=?"
    #db_client.update(sql, (ip, pid, pid))
    """
    # 生成pid文件
    try:
        if os.path.exists(pid_file):
            with open(pid_file, "w") as f:
                pid=f.read()
                if stats.soft_status(pid):
                    log.log("info", "监控程序正在运行, 请不要重复启动")
                    exit()
                else:
                    f.write(os.getpid())
    except Exception as e:
        log.log("error", "无法生成pid文件:", e)
        exit()
    
    # 启动本地安装和监控程序
    try:
        g1=gevent.spawn(Install, )
        g2=gevent.spawn(Status, )
        gevent_list=[g1, g2]
        gevent.joinall(gevent_list)
    except Exception as e:
        log.log("critical", "监控程序无法启动: %s" % e)





