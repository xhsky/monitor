#!/usr/bin/env python
# coding:utf8
# sky
def a():
    c=2
    print(c)

def b():
    global c = 1
    a()
    

if __name__ == "__main__":
    b()
