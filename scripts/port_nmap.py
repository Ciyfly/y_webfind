#!/usr/bin/python
# coding=UTF-8
'''
@Author: Recar
@Date: 2019-07-16 19:19:29
@LastEditTime: 2019-07-18 11:48:53
'''

import nmap
import sys
import time
sys.path.append("../")
from lib.log import logger
from collections import defaultdict

class PortNmap(object):
    """调用Nmap进行端口扫描
        传入ports 则使用ports的端口进行扫描
        否则使用配置文件中的常见端口进行z
    """
    
    def __init__(self, hosts, ports=None, logger=logger):
        self.hosts = hosts
        self.ports = ports
        self.logger = logger
        if self.ports and type(self.ports) is not list:
            self.logger.error("port type is must list")
            exit(1)
        # ip:[ {port: port_info}]
        self.ip_port_names_dict = defaultdict(list)
    
    def run(self):
        scan_satrt = time.perf_counter()
        self.logger.info("start nmap scan {self.hosts} ports")
        nm = nmap.PortScanner()
        if self.ports:
            # 拼接扫描的端口
            arguments = '-sS -n -p '+','.join([str(port) for port in self.ports])
        else:
            # 没有指定则使用默认的nmap1000个端口
            arguments = '-sS -n --top-ports 1000'
        nm.scan(hosts=self.hosts, arguments=arguments, sudo=True)
        self.logger.debug(nm.command_line())
        for host in nm.all_hosts():
            self.logger.info(f"host: {host}")
            if 'tcp' in nm[host]:
                for port in nm[host]['tcp'].keys():
                    state_port = nm[host]['tcp'][port]['state']
                    name = nm[host]['tcp'][port]["name"]
                    if state_port == "open":
                        self.logger.info(f"port: {port} name: {name}")
                        port_name = {"port": port, "name": name}
                        self.ip_port_names_dict[host].append(port_name)
                self.logger.info("==================")
        scan_end = time.perf_counter() - scan_satrt
        self.logger.info(f"nmap use time:{scan_end:.2f}s")
        return self.ip_port_names_dict
