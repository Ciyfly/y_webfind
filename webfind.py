#!/usr/bin/python
# coding=UTF-8
'''
@Author: ysy
@Date: 2019-07-12 15:21:58
@LastEditTime: 2019-08-11 17:45:16
'''
from lib.parser import get_options
from lib.log import logger
from lib.core import  PortScan, WriteOutput, WebInfoScan, WeakPassword
import logging

def main():
	options = get_options()
	domain = options.domain
	domains_file_path = options.domains_file_path
	webinfo = options.webinfo
	port_scan = options.port_scan
	net_c = options.net_c
	all_ports = options.all_ports
	weak_scan = options.weak_scan
	debug = options.debug
	webinfos_dict = None
	ip_port_names_dict =  None
	if debug:
		logger.setLevel(logging.DEBUG)
	if webinfo or not webinfo  and not port_scan: # 默认只进行webinfo获取
		logger.info("web scan\n")
		webinfos_dict = WebInfoScan(domain=domain, domains_file_path=domains_file_path).run()
	if port_scan:
		ip_port_names_dict  = PortScan(domain=domain, domains_file_path=domains_file_path, net_c=net_c, all_ports=all_ports).run()
		if webinfo: # 对端口扫描后的进行web服务探测
			webinfos_dict = WebInfoScan(ip_port_names_dict=ip_port_names_dict).run()
			
	wout = WriteOutput(
		domain=domain, domains_file_path=domains_file_path,
		webinfos_dict=webinfos_dict, ip_port_names_dict=ip_port_names_dict
		)
	# 写数据
	wout.save()
	# 弱口令
	if weak_scan:
		port_and_weak_info = WeakPassword(ip_port_names_dict).run()

# 这里重新写把弱口令也写进去
	wout = WriteOutput(
		domain=domain, domains_file_path=domains_file_path,
		webinfos_dict=webinfos_dict, ip_port_names_dict=port_and_weak_info
	)
	wout.save()	
	
	
if __name__ == "__main__":
	main()
	
	
