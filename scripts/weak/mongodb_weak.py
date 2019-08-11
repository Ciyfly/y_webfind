#!/usr/bin/python
# coding=UTF-8
'''
@Author: Recar
@Date: 2019-07-31 22:27:04
@LastEditTime: 2019-08-08 16:26:42
'''
# resis 弱口令
import os
import sys
base_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(base_path, "../"))
from weak import Base
import pymongo

class Weak(Base):

    def __init__(self, host, port):
        super().__init__(host, port)
        self.name = "mongodb"
        
    def connect(self, username, passwd):
        try:
            myclient = pymongo.MongoClient(f'mongodb://{username}:{passwd}@{self.host}:{self.por}/')
            if res.echo("sec_scan") == "sec_scan":
                self.waek_result["weak"] = True
                self.waek_result["username"] = username
                self.waek_result["passwd"] = passwd
        except Exception:
            pass
