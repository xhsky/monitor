#!/usr/bin/env python
# coding:utf8
# sky

import os, sys
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from conf import version
import tarfile


class install(object):
    def __init__(self):
        pass
    
    def extra(self, pkg_file, dirs):
        t=tarfile.open(pkg_file)
        t.extractall(path=dirs)

if __name__ == "__main__":

    a=install()
    a.extra("../share/package/nginx-1.14.1-bin.tar.gz1", "../test/aaa")
