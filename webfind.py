#!/usr/bin/python
# coding=UTF-8
'''
@Author: ysy
@Date: 2019-07-12 15:21:58
@LastEditTime: 2019-07-31 17:04:30
'''
from lib.parser import get_options
from lib.log import logger
from lib.core import  PortScan, WriteOutput, WebInfoScan
import logging

def main():
	options = get_options()
	domain = options.domain
	domains_file_path = options.domains_file_path
	webinfo = options.webinfo
	port_scan = options.port_scan
	net_c = options.net_c
	all_ports = options.all_ports
	debug = options.debug
	webinfos_list = None
	ip_port_names_list =  None
	if debug:
		logger.setLevel(logging.DEBUG)
	if webinfo or not webinfo  and not port_scan: # 默认只进行webinfo获取
		logger.info("web scan\n")
		webinfos_list = WebInfoScan(domain=domain, domains_file_path=domains_file_path).run()
	if port_scan:
		ip_port_names_list  = PortScan(domain=domain, domains_file_path=domains_file_path, net_c=net_c, all_ports=all_ports).run()

	WriteOutput(domain=domain, domains_file_path=domains_file_path, webinfos_list=webinfos_list, ip_port_names_list=ip_port_names_list)
	
if __name__ == "__main__":
	main()
	
	
