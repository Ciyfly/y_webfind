#!/usr/bin/python
# coding=UTF-8
'''
@Author: Recar
@Date: 2019-07-12 16:10:15
@LastEditTime: 2019-07-12 16:28:55
'''


import os
import subprocess

def is_alive(target):
    cmd = "ping -c 1 -w 1 {}".format(target)
    # status = os.system(cmd)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True) 
    p.wait()
    result_lines = p.stdout.readlines()   # 从子进程 p 的标准输出中读取所有行，并储存在一个list对象中

