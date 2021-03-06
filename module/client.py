#!/usr/bin/env python
# coding:utf8
# sky

import paramiko
import socket, os
from module import logger

class client(object):
    def __init__(self, port=22, username="root"):
        self.__port=port
        self.__user=username
        self.__log=logger.logger()
        self.__ssh=paramiko.SSHClient()
        self.__ssh.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())

    def port_conn(self, ip):
        sk=socket.socket()
        sk.settimeout(1)
        try:
            sk.connect((ip, self.__port))
            res=0
        except Exception as e:
            res=1
        sk.close()
        return res

    def password_conn(self, hostname, password): 
        stat=0
        try:
            self.__ssh.connect(hostname, port=self.__port, username=self.__user, password=password, timeout=1)
            self.__log.log("info", "%s 正常连接" % hostname)
            stat=1
        except paramiko.ssh_exception.NoValidConnectionsError as e:
            self.__log.log("error", "无法连接, 请检查%s的%s端口: %s" % (hostname, self.__port, e))
            stat="%s: 端口无法连接" % hostname
        except paramiko.ssh_exception.AuthenticationException as e:
            self.__log.log("error", "无法连接, 请检查%s的%s密码: %s" % (hostname, self.__user, e))
            stat="%s: 密码错误" % hostname
        except Exception as e:
            self.__log.log("error", "无法连接, 连接%s产生未知错误: %s" % (hostname, e))
            stat="%s: 未知错误" % hostname
        self.__ssh.close()
        return stat

    def gen_keys(self, key_dir="./data/keys"):
        """生成公私钥对"""
        self.__key_dir=key_dir
        pkey_file="%s/sky_pkey" % self.__key_dir
        pkey_pub_file="%s/sky_pkey.pub" % self.__key_dir

        if os.path.exists(pkey_file) and os.path.exists(pkey_pub_file):
            pass
        else:
            # 生成私钥文件
            key=paramiko.rsakey.RSAKey.generate(2048)
            key.write_private_key_file(pkey_file)
            # 生成公钥文件
            pub_key_file=key.get_base64()
            pub_key_sign="%s%s" % (" ".join(["ssh-rsa", pub_key_file]), "\n")
            with open(pkey_pub_file, "w") as f:
                f.write(pub_key_sign)
            self.__log.log("info", "已生成公私钥")

    def key_conn(self, hostname, password):
        pub_key_file="%s/sky_pkey.pub" % self.__key_dir

        with open(pub_key_file, "r") as f:
            pub_key=f.read()

        self.__ssh.connect(hostname, port=self.__port, username=self.__user, password=password, timeout=1)
        self.__ssh.exec_command("setenforce 0; mkdir -p ~/.ssh; chmod 700 ~/.ssh")
        
        sftp=self.__ssh.open_sftp()
        sftp_file=sftp.file("./.ssh/authorized_keys", "a")
        sftp_file.write(pub_key)
        sftp_file.chmod(384)
        sftp_file.close()
        sftp.close()
        self.__log.log("info", "%s 已完成免密码通信" % hostname)

    def exec(self, hostname, commands):
        pkey_file="%s/sky_pkey" % self.__key_dir
        self.__ssh.connect(hostname, port=self.__port, username=self.__user, key_filename=pkey_file, timeout=1)
        self.__ssh.exec_command(commands)
        
    def transfer(self, hostname, local_file, remote_file, remote_path):
        pkey_file="%s/sky_pkey" % self.__key_dir
        self.__ssh.connect(hostname, port=self.__port, username=self.__user, key_filename=pkey_file, timeout=1)
        sftp=self.__ssh.open_sftp()
        sftp.put(local_file, remote_file, confirm=True)
        self.__log.log("info", "安装包传输至%s:%s" % (hostname, remote_path))
        tar_command="tar -xf %s -C %s" % (local_file, remote_path)
        self.__ssh.exec_command(tar_command)
        self.__log.log("info", "%s上的安装包解压至%s" % (hostname, remote_path))
       sftp.close()

    def __del__(self):
        self.__ssh.close()

if __name__ == "__main__":
    #a={"192.168.1.122":"test1", "192.168.1.123":'test2'}
    #b=password_conn(a, username="test1")
    #print(b)

    #gen_keys()
    gen_keys()
    key_conn("192.168.1.123", "root", "111111")

