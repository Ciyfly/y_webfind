#!/usr/bin/python
# coding=UTF-8
'''
@Author: Recar
@Date: 2019-07-31 22:06:49
@LastEditTime: 2019-08-09 18:43:18
'''
# mysql弱口令

import os
import sys
base_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(base_path, "../"))
from weak import Base
import psycopg2



class Weak(Base):

    def __init__(self, host, port):
        super().__init__(host, port)
        self.name = "postgresql"

    def connect(self, username, passwd):
        try:
            conn=psycopg2.connect(
                database="postgres",user=username,
                password=passwd,host=self.host,port=self.port
                )
            self.waek_result["weak"] = True
            self.waek_result["username"] = username
            self.waek_result["passwd"] = passwd
        except Exception:
            pass
