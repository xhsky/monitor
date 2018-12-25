#!/usr/bin/env python
# coding:utf8
# sky

import paramiko
import socket
from module import logger, basedir


base_dir=basedir.base_dir()

class client(object):
    def __init__(self, port=22, username="root"):
        self.port=port
        self.user=username
        self.log=logger.logger()

    def password_conn(self, host_dict): 
        """校验端口连通和密码正确性, host_dict为 hostname:password 的字典, 返回 hostname:N 的字典"""
        ssh=paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())

        N=0     # 正常的主机数
        for i in host_dict.keys():                  
            try:
                ssh.connect(hostname=i, port=self.port, username=self.user, password=host_dict[i], timeout=1)
                self.log.log("info", "%s 正常连接" % i)
                N+=1
            except paramiko.ssh_exception.NoValidConnectionsError as e:
                self.log.log("error", "无法连接, 请检查%s的%s端口: %s" % (i, self.port, e))
            except paramiko.ssh_exception.AuthenticationException as e:
                self.log.log("error", "无法连接, 请检查%s的%s密码: %s" % (i, self.user, e))
            except Exception as e:
                self.log.log("error", "无法连接, 连接%s产生未知错误: %s" % (i, e))
        ssh.close()

        if N==len(host_dict):
            return 1
        else:
            return 0

    def gen_keys(self, key_dir="%s/data/keys" % base_dir):
        self.__key_dir=key_dir
        """生成公私钥对"""

        pkey="%s/sky_pkey" % self.__key_dir
        pkey_pub="%s/sky_pkey.pub" % self.__key_dir
        key=paramiko.rsakey.RSAKey.generate(2048)
        key.write_private_key_file(pkey)
        pub_key=key.get_base64()
        pub_key_sign="%s%s" % (" ".join(["ssh-rsa", pub_key]), "\n")
        with open(pkey_pub, "w") as f:
            f.write(pub_key_sign)
            self.log.log("info", "已生成公私钥")

    def key_conn(self, host_dict):
        ssh=paramiko.SSHClient()
        pub_key_file="%s/sky_pkey.pub" % self.__key_dir

        with open(pub_key_file, "r") as f:
            pub_key=f.read()
        for i in host_dict:
            ssh.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
            ssh.connect(hostname=i, port=self.port, username=self.user, password=host_dict[i], timeout=1)
            ssh.exec_command("setenforce 0; mkdir -p ~/.ssh; chmod 700 ~/.ssh")
            
            sftp=ssh.open_sftp()
            sftp_file=sftp.file("./.ssh/authorized_keys", "a")
            sftp_file.write(pub_key)
            sftp_file.chmod(384)
            sftp_file.close()
            sftp.close()
            ssh.close()
            self.log.log("info", "%s 已完成免密码通信" % i)

            """
            ssh.connect(hostname, port=port, username=username,key_filename="./sky_pkey", timeout=1)
            stdin, stdout, stderr=ssh.exec_command("ls -l ./.ssh/")
            print(stdout.read().decode())
            """

if __name__ == "__main__":
    #a={"192.168.1.122":"test1", "192.168.1.123":'test2'}
    #b=password_conn(a, username="test1")
    #print(b)

    #gen_keys()
    gen_keys()
    key_conn("192.168.1.123", "root", "111111")

