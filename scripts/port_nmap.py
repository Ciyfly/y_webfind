#!/usr/bin/python
# coding=UTF-8
'''
@Author: Recar
@Date: 2019-07-16 19:19:29
@LastEditTime: 2019-07-17 21:56:58
'''

import nmap
import sys
import time
sys.path.append("../")
from lib.log import logger
from collections import defaultdict
from config.config import SCAN_PORTS

class PortNmap(object):
    """调用Nmap进行端口扫描
        传入ports 则使用ports的端口进行扫描
        否则使用配置文件中的常见端口进行z
    """
    
    def __init__(self, hosts, ports=SCAN_PORTS, logger=logger):
        self.hosts = hosts
        self.ports = ports
        self.logger = logger
        if type(self.ports) is not list:
            self.logger.error("port type is must list")
        # ip:[ {port: port_info}]
        self.ip_port_names_dict = defaultdict(list)
    
    def run(self):
        scan_satrt = time.perf_counter()
        self.logger.info("start nmap scan ports")
        nm = nmap.PortScanner()
        # 拼接扫描的端口
        arguments = ' -n -p '+','.join([str(port) for port in self.ports])
        nm.scan(hosts=self.hosts, arguments=arguments)
        self.logger.debug(nm.command_line())
        for host in nm.all_hosts():
            self.logger.debug(f"host: {host}")
            if 'tcp' in nm[host]:
                for port in nm[host]['tcp'].keys():
                    state_port = nm[host]['tcp'][port]['state']
                    name = nm[host]['tcp'][port]["name"]
                    if state_port == "open":
                        self.logger.debug(f"port: {port} name: {name}")
                        port_name = {"port": port, "name": name}
                        self.ip_port_names_dict[host].append(port_name)
                self.logger.debug("==================")
        scan_end = time.perf_counter() - scan_satrt
        self.logger.info(f"nmap use time:{scan_end:.2f}s")
        return self.ip_port_names_dict
