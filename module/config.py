#!/usr/bin/env python
# coding:utf8
# sky

"""
配置文件
"""

import logger

class config(object):
    def __init__(self, config_file_path):
        self.log=logger.logger()
        self.config_file_path=config_file_path

    def read_config(self):
        try: 
            with open(self.config_file_path, "r", encoding="utf8") as config_file:
                self.config_data=config_file.read()
            self.log.log("info", "读取配置文件%s" % self.config_file_path)
        except Exception as e:
            self.log.log("error", e)

    def write_config(self, config_data):
        try: 
            with open(self.config_file_path, "w", encoding="utf8") as config_file:
                config_file.write(config_data)
            self.log.log("info", "写入配置文件%s" % self.config_file_path)
        except Exception as e:
            self.log.log("error", e)
    def init_config(option_dict):
        pass

if __name__ == "__main__":
    conf=config("../test/aaa.xml")
    #conf.ini_config(a, "../test/my.cnf")
    conf.read_config()
    print(type(conf.config_data))


    conf.write_config(conf.config_data)
