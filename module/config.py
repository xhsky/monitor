#!/usr/bin/env python
# coding:utf8
# sky

"""
配置文件
"""
from module import logger
import yaml

class config(object):
    def __init__(self, config_file_path):
        self.__log=logger.logger()
        self.__config_file_path=config_file_path

    def read_config(self):
        try: 
            with open(self.__config_file_path, "r", encoding="utf8") as config_file:
                self.__config_data=config_file.read()
            self.__log.log("info", "读取配置文件%s" % self.config_file_path)
        except Exception as e:
            self.__log.log("error", e)

    def write_config(self, config_data):
        try: 
            with open(self.__config_file_path, "w", encoding="utf8") as config_file:
                config_file.write(config_data)
            self.__log.log("info", "写入配置文件%s" % self.config_file_path)
        except Exception as e:
            self.__log.log("error", e)
    def init_config(option_dict):
        pass
    def get_monitor_conf(self):
        monitor_config_file=self.__config_file_path
        with open(monitor_config_file, "r", encoding="utf8") as config_file:
            conf=yaml.load(config_file)
        return conf

if __name__ == "__main__":
    conf=config("../test/aaa.xml")
    #conf.ini_config(a, "../test/my.cnf")
    conf.read_config()


    conf.write_config(conf.config_data)
