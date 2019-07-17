#!/usr/bin/python
# coding=UTF-8
'''
@Author: Recar
@Date: 2019-07-12 15:56:41
@LastEditTime: 2019-07-17 21:57:47
''' 

from dns import resolver
from lib.log import logger
from scripts.port_masscan import PortMasscan
from scripts.port_nmap import PortNmap
import re
import os
import subprocess
import requests
import json
import datetime

def domain_to_ip(domain):
    """将域名转为ip"""
    try:
        ans = resolver.query(domain, "A")
        if ans:
            for i in ans.response.answer:
                for j in i.items:
                    if hasattr(j, "address"):
                        return j.address
    except Exception as e:
        return None


def get_ip_target(target):
    """对传入的目标参数进行判断解析成ip形式"""
    if not re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', target):
        target = domain_to_ip(target)
    if target:
        if is_alive(target):
            logger.info("target ip: "+target)
            return target
        else:
            logger.error("测试目标不存活")
    else:
        logger.error("不能解析测试域名")


def is_alive(target):
    """判断主机是否存活 使用ping的形式"""
    cmd = "ping -c 1 -w 1 {}".format(target)
    # status = os.system(cmd)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True) 
    p.wait()
    status = p.returncode
    if status: #1 执行失败
        return False
    else:
        return True


class PortScan(object):
    """对c段进行扫描 如果all_ports=True 使用masscan进行端口扫描后交给nmap进行服务识别              
        否则直接使用nmap进行常见端口扫描   

        args:
        
        net_c: 是否对c段进行扫描  defalue=False
        
        all_ports: 是否对全端口进行扫描  defalue=False
        
        logger: 传入日志对象 不传入默认使用webfind自己的

        usage:

        >>> pos = PortScan(target_ip, net_c=True, all_ports=True)

        >>> ip_port_names_dict = pos.scan() # host:[{"port":port,"name":name}]

    """
    def __init__(self, target_ip, net_c=False, all_ports=False, logger=logger):
        self.hosts = target_ip
        self.net_c = net_c
        self.all_ports = all_ports
        self.logger = logger
    
    def scan(self):
        logger.info("port scan")
        if self.net_c:
            logger.info("C segment port scan")
            self.hosts = self.hosts+"/24"
        if self.all_ports:
            # masscan 先扫描一下存活的端口交给nmap再详细扫描
            pmscan = PortMasscan(self.hosts, logger=self.logger)
            open_ports = pmscan.run()
            # nmapscan
            pnscan = PortNmap(self.hosts, ports=open_ports, logger=self.logger)
            ip_port_names_dict = pnscan.run()
            self.logger.info("port scan end")
            return ip_port_names_dict
        else:# 否则直接交给Nmap扫描 配置文件中的常见端口
            pnscan = PortNmap(self.hosts, logger=self.logger)
            ip_port_names_dict = pnscan.run()
            self.logger.info("port scan end")
            return ip_port_names_dict

# def get_title(ip_port_names_dict):
#     for host in ip_port_names_dict.keys():
#         port_names = ip_port_names_dict[host]
#         for port_name in port_names:
#             port = port_name["port"]
#             name = port_name["name"]
#             if name == "http" or "https":
#                 response = requests.get(f"{name}:{host}:{port}")
#                 status_code = response.status_code()
#                 title = re.findall('<title>[\s\S]*?</title>', response.content)[0]
                

def subdomain_to_c(subdomain_log_path):
    ips_c = set()
    with open(subdomain_log_path, "r") as f:
        for domain_ips in f:
            domain = domain_ips.split("    ")[0]
            ip_list = eval(domain_ips.split("    ")[1])
            for ip in ip_list:
                ip_split = ip.split(".")
                ip_c = f"{ip_split[0]}.{ip_split[1]}.{ip_split[2]}.0/24"
                ips_c.add(ip_c)
    logger.info(f"find c segment count: {len(ips_c)}")
    return ips_c

def write_output(data, ip_c, domain=None):
    ip_c = ip_c.replace("/24", "")
    if domain is None:
        domain = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    base_path = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_path, "../", "output", domain)
    output_path = f"{output_dir}/{ip_c}.json"
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    with open(output_path, "w") as f:
        json.dump(data, f, indent=3)
    logger.info(f"save {ip_c} to {output_path}")
