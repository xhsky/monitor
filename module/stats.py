#!/usr/bin/env python
# coding:utf8
# sky

import psutil, time

class soft_status(object):
    def __init__(self, pid):
        self.__pid=pid

    def pid_exist(self):
        res=psutil.pid_exists(self.__pid)
        return res

    def info(self):
        process=psutil.Process(self.__pid)
        info_list=["pid", "create_time", "connections", "num_threads", "cpu_percent", "memory_percent", "username"]
        info_dict=process.as_dict(attrs=info_list)
        info_dict["time"]=time.time()
        info_dict["connections"]=len(info_dict["connections"])
        return info_dict

class host_status(object):
    def __init__(self):
        pass
    def cpu_num(self):
        cpu_num={'time':time.time()}
        cpu_num['cpu_physical_core']=psutil.cpu_count(logical=False)
        cpu_num['cpu_logic_core']=psutil.cpu_count()
        return cpu_num

    def cpu_util(self, interval):
        cpu_percent=psutil.cpu_percent(interval)
        cpu_util={
                "time": time.time(), 
                "cpu_percent": cpu_percent
                }
        return cpu_util

    def mem_size(self):
        mem_size={'time':time.time()}
        mem_size['total']=psutil.virtual_memory()[0]
        mem_size['swap_total']=psutil.swap_memory()[0]
        return mem_size

    def mem_util(self):
        temp1=psutil.virtual_memory()
        temp2=psutil.swap_memory()
        
        mem_util={
                "time": time.time(), 
                "available": temp1[1], 
                "percent": temp1[2], 
                "used": temp1[3], 
                "free": temp1[4], 
                "buffers": temp1[7],
                "cache": temp1[8], 
                "shared": temp1[9], 
                "swap_used": temp2[1], 
                "swap_used": temp2[2], 
                "swap_percent": temp2[3]
                }
        return mem_util

    def disk_info(self):
        disk_info={'time':time.time()}
        temp=psutil.disk_partitions()
        for i, disk in enumerate(temp, start=1):
            disk_info[disk[1]]={
                    "device": disk[0], 
                    "fstype": disk[2], 
                    "total": psutil.disk_usage(disk[1])[0]
                    }
        return disk_info

    def disk_util(self):
        disk_util={'time':time.time()}
        temp=psutil.disk_partitions()
        for disk in temp:
            single_disk_util=psutil.disk_usage(disk[1])
            disk_util[disk[1]]={
                    "used": single_disk_util[1], 
                    "free": single_disk_util[2], 
                    "percent": single_disk_util[3]
                    }
        return disk_util

    def network_io(self, interval):
        start_io=psutil.net_io_counters()
        time.sleep(interval)
        end_io=psutil.net_io_counters()
        network_io={"time":time.time()}
        network_io["bytes_sent"]=int((end_io[0]-start_io[0])/interval)
        network_io["bytes_recv"]=int((end_io[1]-start_io[1])/interval)
        return network_io

    def disk_io(self, interval):
        start_io=psutil.disk_io_counters()
        time.sleep(interval)
        end_io=psutil.disk_io_counters()
        disk_io={"time":time.time()}
        disk_io["read_bytes"]=int((end_io[2]-start_io[2])/interval)
        disk_io["write_bytes"]=int((end_io[3]-start_io[3])/interval)
        return disk_io

    def users(self):
        users={"time":time.time()}
        temp=psutil.users()
        for i, user in enumerate(temp, start=1):
            users["user%s" % i]={
                    "name": user[0], 
                    "terminal": user[1], 
                    "host": user[2], 
                    "started": user[3]
                    }
        return users

if __name__ == "__main__":
    pass
