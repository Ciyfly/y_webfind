#!/usr/bin/python
# coding=UTF-8
'''
@Author: Recar
@Date: 2019-07-16 18:30:00
@LastEditTime: 2019-07-18 14:11:46
'''

import time
import sys
sys.path.append("../")
from lib.log import logger
from scripts.masscan import PortScanner 

class PortMasscan(object):
    """masscan 适用于全端口的扫描 将结果再进一步交给nmap对指定端口进行扫描识别"""
    """
    hosts: 测试的目标 ip或者c段 1.1.1.1/1.1.1.1/24

    ports: 测试的端口 默认是全端口 传入是list类型

    logger: 日志对象 用于内部日志输出 默认使用自己的
    """
    def __init__(self, hosts, ports=None, logger=logger):
        self.hosts = hosts
        self.ports = ports
        self.logger = logger
        if ports: # 将端口列表拼接成 以逗号隔开的字符串
            self.ports = ','.join([str(port) for port in self.ports])
        # [{ip:[22, 80]}]
        self.host_open_port_list = list()
    
    def run(self):
        scan_satrt = time.perf_counter()
        self.logger.info(f"start masscan {self.hosts} all ports")
        mas = PortScanner()
        arguments='--rate 1000'
        if self.ports is None:
            mascscan_result = mas.scan(self.hosts, arguments=arguments ,sudo=True)
        else:
            mascscan_result = mas.scan(self.hosts, ports=self.ports, arguments=arguments, sudo=True)
        command_line = mascscan_result['masscan']['command_line']
        self.logger.debug(f"masscan commend: {command_line}")
        scan_result = mascscan_result['scan']
        for host in scan_result.keys():
            open_ports = list()
            for port in scan_result[host]['tcp'].keys():
                open_ports.append(port)
            self.host_open_port_list.append({"host": host, "open_ports":open_ports})
        scan_end = time.perf_counter() - scan_satrt
        self.logger.info(f"masscan use time:{scan_end:.2f}s")
        self.logger.info(f"open host count: {len(self.host_open_port_list)}")
        return self.host_open_port_list
