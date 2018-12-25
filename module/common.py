#!/usr/bin/env python
# coding:utf8
# sky

import os, sys
import socket
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

if __name__ == "__main__":
    pass
