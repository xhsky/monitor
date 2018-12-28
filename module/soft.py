#!/usr/bin/env python
# coding:utf8
# sky

import tarfile, os, time
from module import logger, stats

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
            return 0
        except Exception as e:
            self.__log.log("error", "软件无法解压, 请重试!: %s" % e)
            return 1
    def init(self):
        # 更改软件目录用户
        soft_dir="%s/%s" % (self.__install_dir, self.__soft_name)
        os.system('chown -R %s:%s %s' % (self.__user, self.__user, self.__install_dir))

        # 初始化配置文件
        
    def init_data(self):
        if self.__soft_name=="mysql":
            rpm_command="rpm -Uvh %s/monitor/share/package/libaio*" % self.__install_dir
            res=os.system(rpm_command)
            if res==0 or res==256:
                self.__log.log("info", "MySQL依赖包libaio安装成功")
                command="%s/mysql/bin/mysqld --defaults-file=%s/mysql/conf/my.cnf --user=%s --initialize" % (self.__install_dir, self.__install_dir, self.__user)
                res=os.system(command)
                if res==0:
                    self.__log.log("info", "mysql初始化完成")
                else:
                  self.__log.log("error", "mysql初始化失败")
            else: 
                self.__log.log("error", "MySQL依赖包libaio无法安装, MySQL无法初始化")

    def set_env(self):
        self.__log.log("info", "启动 %s..." % self.__soft_name)
        os.system("ulimit -n 65536")
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
                os.system(start_command)
            elif self.__soft_name=="mysql":
                os.system(start_command)
            else:
                start_command="su %s -c '%s'" % (self.__user, start_command)
                os.system(start_command)
            time.sleep(1)
            try:
                with open(pid_file, "r") as f:
                    pid=f.read().strip()
                    self.__log.log("info", "%s已启动, Pid: %s" % (self.__soft_name, pid))
                    return pid
            except Exception as e:
                self.__log.log("error", "%s无法启动, 查看相关日志!" % self.__soft_name)
        except Exception as e:
            self.__log.log("error", "%s无法启动: %s" % (self.__soft_name, e))
        return 0

    def start(self):
        if self.__soft_name=="redis":
            start_command="%s/redis/bin/redis-server %s/redis/conf/redis.conf" % (self.__install_dir, self.__install_dir)
            pid_file="%s/redis/redis.pid" % self.__install_dir
            pid=self.read_pid(start_command, pid_file)
        elif self.__soft_name=="nginx":
            start_command="%s/nginx/sbin/nginx" % self.__install_dir
            pid_file="%s/nginx/logs/nginx.pid" % self.__install_dir
            pid=self.read_pid(start_command, pid_file)
        elif soft.__soft_name=="tomcat":
            start_command="%s/tomcat/bin/catalina.sh start" % self.__install_dir
            pid_file=os.getenv("CATALINA_PID")
            pid=self.read_pid(start_command, pid_file)
        elif soft.__soft_name=="mysql":
            start_command="%s/mysql/bin/mysqld_safe --defaults-file=%s/mysql/conf/my.cnf --user=mysql" % (self.__install_dir, self.__install_dir)
            pid_file="%s/mysql/logs/mysqld.pid" % self.__install_dir
            pid=self.read_pid(start_command, pid_file)

        return pid

    def stop(self, pid):
        pid=int(pid)
        status=stats.soft_status(pid)
        self.__log.log("info", "%s正在关闭..." % self.__soft_name)
        N=0
        while N<60:
            try:
                if status.pid_exist():
                    os.kill(pid, 15)
                    time.sleep(1)
                else:
                    self.__log.log("info", "%s已关闭" % self.__soft_name)
                    return 0
            except ProcessLookupError as e:
                self.__log.log("info", "%s已关闭" % self.__soft_name)
                return 0
            N+=1
        self.__log.log("error", "%s无法关闭, 请手动关闭" % self.__soft_name)

if __name__ == "__main__":

    a=install()
    a.extra("../share/package/nginx-1.14.1-bin.tar.gz1", "../test/aaa")
