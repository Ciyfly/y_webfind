#!/usr/bin/python
# coding=UTF-8
'''
@Author: Recar
@Date: 2019-07-31 22:06:49
@LastEditTime: 2019-08-07 22:37:53
'''
# mysql弱口令

import os
import sys
base_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(base_path, "../"))
import pymysql
from weak import Base

class Weak(Base):

    def __init__(self, host, port):
        super().__init__(host, port)
        self.namepasswd_dict_path = os.path.join(self.base_path, "../", "config", "weak","mysql.conf")

    def connect(self, username, passwd):
        try:
            conn = pymysql.connect(
                host=self.host, port=self.port,
                user=username, password=passwd,
                timeout=5
                )
            self.waek_result["weak"] = True
            self.waek_result["username"] = username
            self.waek_result["passwd"] = passwd
        except Exception:
            pass
