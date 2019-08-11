#!/usr/bin/python
# coding=UTF-8
'''
@Author: Recar
@Date: 2019-08-07 19:46:36
@LastEditTime: 2019-08-09 18:45:15
'''
import os
import sys
import time
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
        self.thread = True
        self.sleep_time = 0
        self.name_passwd = list()
        # 字典
        self.username_dict_path = os.path.join(self.base_path, "../", "config", "weak","username.conf")
        self.password_dict_path = os.path.join(self.base_path, "../", "config", "weak","password.conf")
        # 加载字典
        self.load_dict()
        self.waek_result = {"weak": False,"name": "", "passwd": ""}
    
    def load_dict(self):
        # load dict
        with open(self.username_dict_path, "r") as usernames:
            with open(self.password_dict_path, "r") as passwords:
                for username in usernames:
                    for passwd in passwords:
                        self.name_passwd.append({"username": username.strip(), "passwd": passwd.strip()})

    def run(self):
        try:
            threads = list()
            for name_passwd in self.name_passwd:
                username = name_passwd["username"]
                passwd = name_passwd["passwd"]
                logger.debug(f"{self.name}:{self.host}:{self.port}->{username}:{passwd}")
                # 这里多线程启动 
                if self.thread:
                    t = Thread(target=self.connect,args=(username, passwd))
                    threads.append(t)
                else:# 对于类似ssh的有限制 不进行多线程且增加延迟时间
                    self.connect(username, passwd)
                    if self.sleep_time:
                        time.sleep(self.sleep_time)
            if threads:
                for t in threads:
                    t.start()
        except Exception as e:
            logger.error(e)
        return self.waek_result