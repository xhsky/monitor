#!/usr/bin/env python
# coding:utf8
# sky

conn_host_info_key="conn_host_info" 
"""
dict 前端发送加入集群的主机
{
    ip: password, 
    ip: password
    ...
}
"""
host_soft_info_key="host_soft_info"
"""
dict, 后台记录集群中的主机及其软件名, pid
    {
        ip1:{
            "redis": 0, 
            "tomcat": 1511
            ...
        }, 
        ip2:{
            "redis": 0, 
            "mysql": 1512
            ...
        } 
"""
error_host_conn_key="host_error"    # list(按队列使用), 后端发送的无法连接的ip
"""
{
    ip: "无法连接的原因", 
    ip: "无法连接的原因"
}
"""
stat_info_key="stat_info"           # 订阅发布模式, 记录前端发送的4种主机和软件记录状态
"""
记录软件资源启动
{
    "ip": "192.168.1.114", 
    "type": "soft", 
    "action": "start", 
    "soft_name": {
        "tomcat": [1, 2],                # 记录间隔, 保留时长(小时)
        "redis": [1, 2]
    }
}
记录软件资源关闭
{
    "ip": "192.168.1.114", 
    "type": "soft", 
    "action": "stop"
}
记录主机资源启动
{
    "ip": "192.168.1.108", 
    "type": "host", 
    "action": "start", 
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
记录主机资源关闭
{
    "ip": "192.168.1.116", 
    "type": "host", 
    "action": "stop"
}
"""
soft_stat_info_key="stat_info"      # 列表(按队列使用)
"""
实际key名为 `ip`_`soft_name`_stat_info, 记录某个IP下某个软件某时刻的状态
{
    "memory_percent": 0.012828789458873384, 
    "pid": 21408,
    "num_threads": 4,
    "cpu_percent": 0.0,
    "create_time": 1546050098.27,
    "username": "dream",
    "connections": 2,
    "time": 1546051675.2527032
}

"""
soft_install_info_key="soft_install_info"   # 订阅发布模式, 前端安装及控制两种信息
"""
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



if __name__ == "__main__":
    pass
