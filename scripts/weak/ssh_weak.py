#!/usr/bin/python
# coding=UTF-8
'''
@Author: Recar
@Date: 2019-07-31 22:27:04
@LastEditTime: 2019-08-09 18:43:28
'''
# ssh 弱口令
import os
import sys
base_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(base_path, "../"))
from weak import Base
import paramiko
paramiko.util.log_to_file("paramiko.log")
class Weak(Base):

    def __init__(self, host, port):
        super().__init__(host, port)
        self.name = "ssh"

    def connect(self, username, passwd):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(
                hostname=self.host, port=self.port,
                username=username, password=passwd,
                timeout=5, banner_timeout=5, auth_timeout=5
                )
            self.waek_result["weak"] = True
            self.waek_result["username"] = username
            self.waek_result["passwd"] = passwd
        except paramiko.ssh_exception.SSHException:
            pass
        except ConnectionResetError:
            pass
        except EOFError:
            pass
        except Exception:
            pass
