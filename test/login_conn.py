#!/usr/bin/env python
# coding:utf8
# sky

import os, sys
base_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
module_dir="%s/module" % base_dir
sys.path.append(base_dir)
sys.path.append(module_dir)

from module import client
from module import db
import yaml


if __name__ == "__main__":

    test_host={
            "192.168.1.122":"111111", 
            "192.168.1.123":"111111" 
            }
    with open("../conf/monitor.yml", "r") as config_file:
        res=yaml.load(config_file)

    ip=res["db"].get("ip")
    password=res["db"].get("password")
    port=res["db"].get("port")
    db_name=res["db"].get("db_name")

    db_client=db.redis_conn(ip, password, port, db_name)
    conn=db_client.connect()

    host_dict=db_client.list_set("conn_host_info", test_host)

