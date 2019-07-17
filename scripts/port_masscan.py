#!/usr/bin/python
# coding=UTF-8
'''
@Author: Recar
@Date: 2019-07-16 18:30:00
@LastEditTime: 2019-07-17 17:20:33
'''

import time
import sys
sys.path.append("../")
from lib.log import logger
from scripts.masscan import PortScanner 

class PortMasscan(object):
    """masscan 适用于全端口的扫描 将结果再进一步交给nmap对指定端口进行扫描识别"""
    def __init__(self, hosts, ports=None, logger=logger):
        self.hosts = hosts
        self.ports = ports
        self.logger = logger
        if ports: # 将端口列表拼接成 以逗号隔开的字符串
            self.ports = ','.join([str(port) for port in self.ports])
        self.open_ports = set()
    
    def run(self):
        scan_satrt = time.perf_counter()
        self.logger.info("start masscan all ports")
        mas = PortScanner()
        if self.ports is None:
            mascscan_result = mas.scan(self.hosts, sudo=True)
        else:
            mascscan_result = mas.scan(self.hosts, ports=self.ports, sudo=True)
        command_line = mascscan_result['masscan']['command_line']
        self.logger.debug(f"masscan commend: {command_line}")
        scan_result = mascscan_result['scan']
        for host in scan_result.keys():
            for port in scan_result[host]['tcp'].keys():
                self.open_ports.add(port)
        scan_end = time.perf_counter() - scan_satrt
        self.logger.info(f"masscan use time:{scan_end:.2f}s")
        self.logger.info(f"open ports: {self.open_ports}")
        return list(self.open_ports)
