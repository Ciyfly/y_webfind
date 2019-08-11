#!/usr/bin/python
# coding=UTF-8
'''
@Author: Recar
@Date: 2019-07-16 19:19:29
@LastEditTime: 2019-08-08 16:03:20
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
        否则使用配置文件中的常见端口进行
        :param hosts ip列表
        :param ports 要扫描的端口 默认使用常见1000个端口
        :param logger 传入自定义的端口 默认使用自己的
        :return ip_port_info_dict  {ip:ip, port_info: [{port: port_info}, {port: port_info},]}
    """
    
    def __init__(self, hosts, ports=None, logger=logger):
        self.hosts = hosts
        self.ports = ports
        self.logger = logger
        if self.ports and type(self.ports) is not list:
            self.logger.error("port type is must list")
            exit(1)
        # {ip:ip, port_info: [{port: port_info}, {port: port_info},]}
        self.ip_port_info_list = list()
    
    def run(self):
        scan_satrt = time.perf_counter()
        self.logger.info(f"Start Nmap Scan {self.hosts} Ports")
        nm = nmap.PortScanner()
        if self.ports:
            # 拼接扫描的端口
            arguments = '-sS -n -p '+','.join([str(port) for port in self.ports])
        else:
            # 没有指定则使用默认的nmap1000个端口
            arguments = '-sS -n --top-ports 1000'
            # arguments = '-sS -n -p 3306'
        nm.scan(hosts=self.hosts, arguments=arguments, sudo=True)
        self.logger.debug(nm.command_line())
        for host in nm.all_hosts():
            port_info = list()
            self.logger.info(f"host: {host}")
            if 'tcp' in nm[host]:
                for port in nm[host]['tcp'].keys():
                    state_port = nm[host]['tcp'][port]['state']
                    name = nm[host]['tcp'][port]["name"]
                    if state_port == "open":
                        self.logger.info(f"port: {port} service: {name}")
                        port_info.append({"port": port, "service": name})
                self.logger.info("==================")
            if port_info: # 有开放端口
                self.ip_port_info_list.append({"ip": host, "port_info": port_info})
        scan_end = time.perf_counter() - scan_satrt
        self.logger.info(f"Nmap Use Time:{scan_end:.2f}s")
        return self.ip_port_info_list
