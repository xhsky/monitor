#!/usr/bin/env python
# coding:utf8
# sky

import os, sys
base_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
os.chdir(base_dir)
from module import db
import yaml

def conn_host_info():
    conn_host_info_key="conn_host_info"

    dict_key={
      "192.168.1.108": "111111", 
      "192.168.1.114": "111111", 
      "192.168.1.116": "112111", 
      "192.168.1.124": "111111"
      }

    db_client.hmset(conn_host_info_key, dict_key)

if __name__ == "__main__":

    with open("./conf/monitor.yml", "r") as config_file:
        res=yaml.load(config_file)

    ip=res["db"].get("ip")
    password=res["db"].get("password")
    port=res["db"].get("port")
    db_name=res["db"].get("db_name")

    db_client=db.redis_conn(ip, password, port, db_name)
    conn=db_client.connect()

    conn_host_info()




