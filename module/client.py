#!/usr/bin/env python
# coding:utf8
# sky

import paramiko
import socket
import logger

class client(object):
    def __init__(self, port=22, username="root"):
        self.port=port
        self.user=username
        self.log=logger()
    """
    def port_conn(self, host_list):
        """ 检查端口是否连通, 返回ip:N的字典, 0表示能连接, 1表示有问题 """

        sk=socket.socket()
        sk.settimeout(1)

        for i in host_list:
            try:
                sk.connect((i, port))
                self.log.logger("info", "%s正常连接" % i)
            except Exception as e:
                self.log.logger("error", "%s无法连接: %s" % (i, e))
        sk.close()
    """

    def password_conn(self, host_dict): 
        """校验端口连通和密码正确性, host_dict为 hostname:password 的字典, 返回 hostname:N 的字典"""
        ssh=paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())

        for i in host_dict.keys():                  
            try:
                ssh.connect(hostname=i, port=self.port, username=self.user, password=host_dict[i], timeout=1)
                self.log.logger("info", "%s正常连接" % i)
            except paramiko.ssh_exception.NoValidConnectionsError as e:
                self.log.logger("error", "请检查%s的%s端口: %s" % (i, self.port, e))
            except paramiko.ssh_exception.AuthenticationException as e:
                self.log.logger("error", "请检查%s的%s密码: %s" % (i, self.user, e))
            except Exception as e:
                self.log.logger("error", "连接%s产生未知错误: %s" % (i, e))
        ssh.close()
    def gen_keys(self, key_dir):
        """生成公私钥对"""

        pkey="%s/sky_pkey" % key_dir
        key=paramiko.rsakey.RSAKey.generate(2048)
        key.write_private_key_file(pkey)
        pub_key=key.get_base64()
        pub_key_sign="%s%s" % (" ".join(["ssh-rsa", pub_key]), "\n")
        with open(pkey, "w") as f:
            f.write(pub_key_sign)

    def key_conn(self, host_dict):
        ssh=paramiko.SSHClient()

        with open("./sky_pkey.pub", "r") as f:
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

            """
            ssh.connect(hostname, port=port, username=username,key_filename="./sky_pkey", timeout=1)
            stdin, stdout, stderr=ssh.exec_command("ls -l ./.ssh/")
            print(stdout.read().decode())
            """

def test(hostname, user, password, port=22):

    client=paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
    client.connect(hostname, port=port, username=user, password=password)

    a=client.get_host_keys()
    print("a:", a)

    b=client.get_transport()
    print("a:", b)

    c=client.invoke_shell()
    print("c:", c)
    c.exec_command("ls")

    print(c.fileno())
    c.close()


    d=client.load_host_keys("/home/sky/.ssh/known_hosts")
    print("d:", d)

    e=client.load_system_host_keys("/home/sky/.ssh/known_hosts")
    print("e:", e)

    f=client.open_sftp()
    print("f:", f)

    g=client.save_host_keys("./aba")
    print("g:", g)

    client.close()
def pass_free(host_dict, port=22):
    pass

if __name__ == "__main__":
    #a={"192.168.1.122":"test1", "192.168.1.123":'test2'}
    #b=password_conn(a, username="test1")
    #print(b)

    #gen_keys()
    gen_keys()
    key_conn("192.168.1.123", "root", "111111")

