#!/usr/bin/python
# coding=UTF-8
'''
@Author: ysy
@Date: 2019-07-12 15:21:58
@LastEditTime: 2019-07-17 17:10:19
'''
from lib.parser import get_options
from lib.log import logger
from lib.core import get_ip_target, PortScan
import logging

def main():
	options = get_options()
	target = options.target
	net_c = options.net_c
	all_ports = options.all_ports
	debug = options.debug
	if debug:
		logger.setLevel(logging.DEBUG)
	# 判断ip还是域名 
	target_ip = get_ip_target(target)
	pos = PortScan(target_ip, net_c=net_c, all_ports=all_ports)
	ip_port_info_dict = pos.scan()

if __name__ == "__main__":
	main()
