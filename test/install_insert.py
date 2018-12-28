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

    args={
      "ip": "192.168.1.108", 
      "type": "install", 
      "soft_name": ["tomcat", "jdk", "redis", "nginx", "mysql"]
      }
    args={
      "ip": "192.168.1.108", 
      "type": "control", 
      "soft_name": "nginx", 
      "action": "stop"
      }

    db_client.publish("soft_install_info", args)

