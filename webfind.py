#!/usr/bin/python
# coding=UTF-8
'''
@Author: ysy
@Date: 2019-07-12 15:21:58
@LastEditTime: 2019-07-17 22:06:48
'''
from lib.parser import get_options
from lib.log import logger
from lib.core import get_ip_target, PortScan, subdomain_to_c, write_output
import logging

def main():
	options = get_options()
	target = options.target
	domain_log_path = options.domain_log_path
	domain = options.domain
	net_c = options.net_c
	all_ports = options.all_ports
	debug = options.debug
	if debug:
		logger.setLevel(logging.DEBUG)
	if not domain_log_path:
		# 判断ip还是域名 
		target_ip = get_ip_target(target)
		pos = PortScan(target_ip, net_c=net_c, all_ports=all_ports)
		ip_port_info_dict = pos.scan()
		logger.info(ip_port_info_dict)
		write_output(ip_port_info_dict, target_ip, domain=domain)
	else:
		# 对子域名的结果批量测试
		ips_c = subdomain_to_c(domain_log_path)
		for ip_c in ips_c:
			pos = PortScan(ip_c, net_c=True, all_ports=True)
			ip_port_info_dict = pos.scan()
			logger.info(ip_port_info_dict)
			write_output(ip_port_info_dict, target_ip, domain=domain)
if __name__ == "__main__":
	main()
