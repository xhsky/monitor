#!/usr/bin/env python
# coding:utf8
# sky

import os
import sys
import atexit
import time

def deamonize(pid_file=None):
    pid=os.fork()
    if pid:
        sys.exit(0)
    os.chdir("/")
    os.umask(0)
    os.setsid()

    _pid=os.fork()
    if _pid:
        sys.exit(0)

    sys.stdout.flush()
    sys.stderr.flush()

    with open("/dev/null") as read_null, open("/dev/null", "w") as write_null:
        os.dup2(read_null.fileno(), sys.stdin.fileno())
        os.dup2(write_null.fileno(), sys.stdout.fileno())
        os.dup2(write_null.fileno(), sys.stderr.fileno())

    if pid_file:
        with open(pid_file, "w+") as f:
            f.write(str(os.getpid()))
        atexit.register(os.remove, pid_file)


if __name__ == "__main__":
    """
    pid=deamonize("/tmp/a.pid")
    N=1
    print("main pid", os.getpid())
    while N<10:
        N+=1
        with open("/tmp/a.txt", "a") as f:
            f.write("aaa")
        time.sleep(1)
    """
