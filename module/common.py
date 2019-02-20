#!/usr/bin/env python
# coding:utf8
# sky

import os, sys, socket
from module import stats
def base_dir(file_name, if_append_path=0):
    base_dir=os.path.dirname(os.path.abspath(file_name))
    
    if if_append_path:
        sys.path.append(base_dir)

    return base_dir

def host_ip():
    try:
        s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        return ip
    finally:
        s.close()
def pid_file(pid_file):
    """ 生成pid文件 """
    try:
        if os.path.exists(pid_file):
            with open(pid_file, "r", encoding="utf8") as f:
                pid=int(f.read())
            pid_obj=stats.soft_status(pid)
            if pid_obj.pid_exist():
                with open(pid_file, "w", encoding="utf8") as f:
                    pid=str(os.getpid())
                    f.write(pid)
        else:
            with open(pid_file, "w+", encoding="utf8") as f:
                pid=str(os.getpid())
                f.write(pid)
    except Exception as e:
        return e

if __name__ == "__main__":
    pass
