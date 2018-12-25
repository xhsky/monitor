#!/usr/bin/env python
# coding:utf8
# sky

import os, sys
def base_dir(file_name, if_append_path=0):
    base_dir=os.path.dirname(os.path.abspath(file_name))
    
    if if_append_path:
        sys.path.append(base_dir)

    return base_dir

if __name__ == "__main__":
    pass
