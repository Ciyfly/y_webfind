#!/usr/bin/python
# coding=UTF-8
'''
@Author: Recar
@Date: 2019-07-12 15:56:41
@LastEditTime: 2019-07-12 16:23:07
''' 

from dns import resolver
from lib.script import is_alive
import re


def domain_to_ip(domain):
    try:
        ans = resolver.query(domain, "A")
        if ans:
            for i in ans.response.answer:
                for j in i.items:
                    if hasattr(j, "address"):
                        return j.address
    except Exception as e:
        print(e)
        return None
    
def get_ip_target(target):
    if is_alive(target):
        if not re.search(r'Host: \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', target):
            target = domain_to_ip(target)
        print(target)
        return target
    else:
        print("测试目标不存活或者不允许ping")
