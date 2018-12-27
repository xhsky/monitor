#!/usr/bin/env python
# coding:utf8
# sky

import os, sys
base_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
os.chdir(base_dir)
from module import db
import yaml

if __name__ == "__main__":

    with open("./conf/monitor.yml", "r") as config_file:
        res=yaml.load(config_file)

    ip=res["db"].get("ip")
    password=res["db"].get("password")
    port=res["db"].get("port")
    db_name=res["db"].get("db_name")

    db_client=db.redis_conn(ip, password, port, db_name)
    conn=db_client.connect()
    """
    args={
            "ip": "192.168.1.131", 
            "cpu_num": 5, 
            "cpu_util": {
                "interval": 2, 
                "retain_hour": 0.1
                }, 
            "mem_size": 5, 
            "mem_util": {
                "interval": 2, 
                "retain_hour": 0.1
                }, 
            "disk_info": 5, 
            "disk_util": {
                "interval": 2, 
                "retain_hour": 0.01
                }, 
            "network_io": {
                "interval": 2, 
                "retain_hour": 0.1
                }, 
            "disk_io": {
                "interval": 2, 
                "retain_hour": 0.1
                }, 
            "users": 5
            }
    """ 
    args={
            "ip": "192.168.1.108", 
            "disk_io": {
                "interval": 2, 
                "retain_hour": 0.1}
            }

    db_client.publish("host_stat_info", args)

