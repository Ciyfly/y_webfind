#!/usr/bin/python
# coding=UTF-8
'''
@Author: Recar
@Date: 2019-07-31 22:27:04
@LastEditTime: 2019-08-07 22:55:35
'''
# resis 弱口令

import redis

class Weak(Base):

    def __init__(self, host, port):
        super().__init__(host, port)
        self.namepasswd_dict_path = os.path.join(self.base_path, "../", "config", "weak","redis.conf")

    def connect(self, username, passwd):
        try:
            res = redis.StrictRedis(host=self.host,port=self.port,password=passwd)
            if res.echo("sec_scan") == "sec_scan":
                self.waek_result["weak"] = True
                self.waek_result["username"] = username
                self.waek_result["passwd"] = passwd
        except Exception:
            pass
