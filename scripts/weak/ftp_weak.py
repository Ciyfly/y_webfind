#!/usr/bin/python
# coding=UTF-8
'''
@Author: Recar
@Date: 2019-07-31 22:27:04
@LastEditTime: 2019-08-09 18:42:52
'''
# ftp 弱口令
import os
import sys
base_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(base_path, "../"))
from weak import Base
import ftplib

class Weak(Base):

    def __init__(self, host, port):
        super().__init__(host, port)
        self.name = "ftp"

    def connect(self, username, passwd):
        try:
            ftp = ftplib.FTP(self.host, timeout=5)
            ftp.login(username,password)
            ftp.quit()
            self.waek_result["weak"] = True
            self.waek_result["username"] = username
            self.waek_result["passwd"] = passwd
        except Exception:
            pass
