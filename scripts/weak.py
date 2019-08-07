#!/usr/bin/python
# coding=UTF-8
'''
@Author: Recar
@Date: 2019-08-07 19:46:36
@LastEditTime: 2019-08-07 22:27:10
'''
import os
import sys
base_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(base_path, "../","lib"))
from threading import Thread
from lib.core import logger

class Base(object):
    
    def __init__(self, host, port):
        self.logger = logger
        self.base_path = base_path
        self.host = host
        self.port = port
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.name_passwd = list()
        self.waek_result = {"weak": False,"name": "", "passwd": ""}
    
    def load_dict(self):
        # load dict
        with open(self.namepasswd_dict_path, "r") as f:
            for name_passwd in f:
                username = name_passwd.split(":")[0]
                passwd = name_passwd.split(":")[1]
                self.name_passwd.append({"username": username, "passwd": passwd})

    def run(self):
        # 加载字典
        self.load_dict()
        threads = list()
        for name_passwd in self.name_passwd:
            username = name_passwd["username"]
            passwd = name_passwd["passwd"]
            logger.debug(f"{self.host}:{self.port}->{username}:{passwd}")
            # 这里多线程启动 
            t = Thread(target=self.connect,args=(username, passwd))
            threads.append(t)
        for t in threads:
            t.start()
        return self.waek_result