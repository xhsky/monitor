#!/usr/bin/env python
# coding:utf8
# sky

import tarfile, os, time
from module import logger

class install(object):
    def __init__(self, user, soft_name, install_dir):
        self.__log=logger.logger()
        self.__user=user
        self.__soft_name=soft_name
        self.__install_dir=install_dir
    
    def extra(self, pkg_file):
        try:
            t=tarfile.open(pkg_file)
            t.extractall(path=self.__install_dir)
        except Exception as e:
            self.__log.log("error", "软件无法解压, 请重试!")
    def init(self):
        # 更改软件目录用户
        soft_dir="%s%s" % (self.__install_dir, self.__soft_name)
        os.system('chown -R %s:%s %s' % (soft_dir, self.__user, self.__user))

        # 初始化配置文件
        
    def init_data(self):
        if self.__soft_name=="mysql":
            command="%s/mysql/bin/mysqld --defaults-file=/etc/my.cnf --user=%s --initialize" % (self.__install_dir, self.__user)
            os.system(command)
            self.__log.log("info", "mysql初始化完成")

    def set_env(self):
        if self.__soft_name=="redis":
            try: 
                os.system('echo 1024 > /proc/sys/net/core/somaxconn')
                os.system('sysctl vm.overcommit_memory=1')
                os.system('echo never > /sys/kernel/mm/transparent_hugepage/enabled')
                self.__log.log("info", "Redis系统参数已更改")
            except Exception as e:
                self.__log.log("error", "Redis系统参数更改失败: %s" % e)
        elif self.__soft_name=="tomcat":
            os.environ["JAVA_HOME"]="%s/jdk" % self.__install_dir
            os.environ["CATALINA_HOME"]="%s/tomcat" % self.__install_dir
            os.environ["CATALINA_PID"]="%s/tomcat/bin/catalina.pid" % self.__install_dir
        elif self.__soft_name=="mysql":
            # rpm -ivh libaio
            pass

    def read_pid(self, start_command, pid_file):
        try:
            if self.__soft_name=="nginx":
                os.system(start_commond)
            elif self.__soft_name=="mysql":
                os.system(start_commond)
            else:
                start_command="su %s -c '%s'" % (self.__user, start_command)
                os.system(start_commond)
            try:
                with open(pid_file, "r") as f:
                    pid=f.read()
                    self.log.log("info", "%s已启动, Pid: %s" % (self.__soft_name, pid))
                    return pid
            except Exception as e:
                self.__log.log("error", "%s无法启动, 查看相关日志!" % self.__soft_name)
        except Exception as e:
            self.__log.log("error", "%s无法启动: %s" % (self.__soft_name, e))

    def start(self):
        if self.__soft_name=="redis":
            start_commond="%s/redis/bin/redis-server %s/redis/conf/redis.conf" % (self.__install_dir, self.__install_dir)
            pid_file="%s/redis/redis.pid" % self.__install_dir
            pid=self.read_pid(start_command, pif_file)
        elif self.__soft_name=="nginx":
            start_commond="%s/nginx/sbin/nginx" % self.__install_dir
            pid_file="%s/nginx/logs/nginx.pid" % self.__install_dir
            pid=self.read_pid(start_command, pif_file)
        elif soft.__soft_name=="tomcat":
            start_command="%s/tomcat/bin/catalina.sh start" % self.__install_dir
            pid_file=os.getenv("CATALINA_PID")
            pid=self.read_pid(start_command, pif_file)
        elif soft.__soft_name=="mysql":
            start_command="%s/mysql/bin/mysqld_safe --defaults-file=%s/mysql/conf/my.cnf --user=mysql" % (self.__install_dir, self.__install_dir)
            pid_file="%s/mysql/logs/mysqld.pid" % self.__install_dir
            pid=self.read_pid(start_command, pif_file)


        return pid

    def stop(self, soft, pid):
        N=1
        while True:
            try:
                if N==60:
                    self.__log.log("error", "%s无法关闭, 请手动关闭" % soft)
                else:
                    os.kill(pid, 15)
                    time.sleep(1)
                N+=1
                self.__log.log("info", "%s正在关闭..." % soft)
            except ProcessLookupError as e:
                self.__log.log("info", "%s已关闭" % soft)
                break

if __name__ == "__main__":

    a=install()
    a.extra("../share/package/nginx-1.14.1-bin.tar.gz1", "../test/aaa")
