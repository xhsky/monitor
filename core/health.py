#!/usr/bin/env python
# coding:utf8
# sky

from module import heartbeat, config, db, common, logger
import time
import gevent
from gevent import monkey

class health(object):
    def __init__(self):
        self.__heart=heartbeat.heartbeat()
        self.__log=logger.logger()
        self.__res=config.config("./conf/monitor.yml").get_monitor_conf()

    def heart(self):
        # 心跳程序
        heart_time=self.__res["heartbeat_second"]
        timeout_time=self.__res["timeout_second"]
        self.__log.log("info", "心跳程序已开始")
        while True:
            self.__heart.heartbeat_info(heart_time)
            time.sleep(heart_time)

    def check(self):
        # 心跳检查
        base_dir=self.__res["base_dir"]
        self.__log.log("info", "健康程序已开始")
        start_command="%s/python/bin/python3 %s/monitor/main.py" % (base_dir, base_dir)
        while True:
            ip_list=self.__heart.obtain()
            for ip in ip_list:
                os.system(start_command)

def check():
    monkey.patch_all() 

    health_chekc=health()

    try:
        g1=gevent.spawn(health_chekc.heart, )
        g2=gevent.spawn(health_chekc.check, )
        gevent_list=[g1, g2]
        gevent.joinall(gevent_list)
    except Exception as e:
        log.log("critical", "检查无法启动: %s" % e)

if __name__ == "__main__":
    pass
