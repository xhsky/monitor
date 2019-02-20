#!/usr/bin/env python
# coding:utf8
# sky

import time, os, signal

receive_times=0
def handler(signalnum, stack):
    global receive_times
    print("收到信号:", signalnum, receive_times, stack)
    receive_times+=1
    if receive_times>3:
        exit(0)

def main():
    signal.signal(signal.SIGINT, handler)
    while True:
        pass
def main1():
    print("pid:", os.getpid())
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)
    while True:
        pass
if __name__ == "__main__":
    main1()
