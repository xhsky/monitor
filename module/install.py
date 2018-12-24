#!/usr/bin/env python
# coding:utf8
# sky

import tarfile

class install(object):
    def __init__(self):
        pass
    
    def extra(self, pkg_file, dirs):
        t=tarfile.open(pkg_file)
        t.extractall(path=dirs)
    
    def init_data(self):
        pass

    def init_config(self):
        pass

if __name__ == "__main__":

    a=install()
    a.extra("../share/package/nginx-1.14.1-bin.tar.gz1", "../test/aaa")
