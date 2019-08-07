#!/usr/bin/python
# coding=UTF-8
'''
@Author: Recar
@Date: 2019-07-31 22:27:04
@LastEditTime: 2019-08-07 22:38:37
'''
# ssh 弱口令

import paramiko

class Weak(Base):

    def __init__(self, host, port):
        super().__init__(host, port)
        self.namepasswd_dict_path = os.path.join(self.base_path, "../", "config", "weak","ssh.conf")

    def connect(self, username, passwd):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(
                hostname=self.host, port=self.port,
                username=username, password=passwd,
                timeout=5
                )
            stdin, stdout, stderr = ssh.exec_command('whomai')
            ssh.close()
            self.waek_result["weak"] = True
            self.waek_result["username"] = username
            self.waek_result["passwd"] = passwd
        except Exception:
            pass
