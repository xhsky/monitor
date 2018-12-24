#!/usr/bin/env python
# coding:utf8
# sky

import logging.config
import yaml
class logger(object):
    def __init__(self, log_config_file="../conf/logger.yml"):
        with open(log_config_file, "r", encoding="utf8") as f:
            dict_log_conf=yaml.load(f)
        logging.config.dictConfig(dict_log_conf)

        self.record=logging.getLogger()

    def log(self, level, message):
        if level.upper()=="CRITICAL":
            self.record.critical(message)
        elif level.upper()=="ERROR":
            self.record.error(message)
        elif level.upper()=="WARN":
            self.record.warning(message)
        elif level.upper()=="INFO":
            self.record.info(message)
        elif level.upper()=="DEBUG":
            self.record.debug(message)
        else:
            self.record.error("无该日志记录级别. %s" % message)
            

if __name__ == "__main__":
    logs=logger("../config/logger.yml")
    logs.log("debug", "哈哈哈哈")
    logs.log("info", "哈哈哈哈")
    logs.log("warn", "哈哈哈哈")
    logs.log("error", "哈哈哈哈")
    logs.log("critical", "哈哈哈哈")
