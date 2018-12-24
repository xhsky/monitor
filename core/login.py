#!/usr/bin/env python
# coding:utf8
# sky

import os, sys
base_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#module_dir="%s/module" % base_dir
sys.path.append(base_dir)
#sys.path.append(module_dir)

from module import client
from module import db
import yaml, json


if __name__ == "__main__":
    with open("../conf/monitor.yml", "r") as config_file:
        res=yaml.load(config_file)

    ip=res["db"].get("ip")
    password=res["db"].get("password")
    port=res["db"].get("port")
    db_name=res["db"].get("db_name")

    host_client=client.client()
    db_client=db.redis_conn(ip, password, port, db_name)
    conn=db_client.connect()
    #print(ip, password, port, db_name)
    #a=db_client.str_get("192.168.1.131_users")
    #print(a)

    # conn_host_info 为redis中的list, 存储hostname:password的字典
    host_dict=db_client.list_get("conn_host_info")
    if host_dict is not None:
        stats=host_client.password_conn(host_dict)
        if stats:
            host_client.gen_keys()
            host_client.key_conn(host_dict)

