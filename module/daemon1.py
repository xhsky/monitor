#!/usr/bin/env python
# coding:utf8
# sky

import daemon
import lockfile
import time, os, sys

if __name__ == "__main__":
    print(os.getpid())
    with daemon.DaemonContext(
            working_directory="/",
            stdout=sys.stdout, 
            stderr=sys.stderr
            ):
        N=1
        while N<10:
            with open("a.log", "a") as f:
                f.write(os.getpid())
            time.sleep(1)
            N+=1
