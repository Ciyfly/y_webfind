#!/usr/bin/python
# coding=UTF-8
'''
@Author: ysy
@Date: 2019-07-12 15:21:58
@LastEditTime: 2019-07-12 16:19:01
'''
from lib.parser import get_options
from lib.core import get_ip_target
def main():
    options = get_options()
    target = options.target
    # 判断ip还是域名 
    if get_ip_target(target):
        # 是ip -> 判断是否存活 -> 是否cdn->进行端口扫描和c段获取
        pass

if __name__ == "__main__":
    main()