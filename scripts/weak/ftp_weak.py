#!/usr/bin/python
# coding=UTF-8
'''
@Author: Recar
@Date: 2019-07-31 22:27:04
@LastEditTime: 2019-08-07 22:38:10
'''
# ftp 弱口令

import ftplib

class Weak(Base):

    def __init__(self, host, port):
        super().__init__(host, port)
        self.namepasswd_dict_path = os.path.join(self.base_path, "../", "config", "weak","ftp.conf")

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
