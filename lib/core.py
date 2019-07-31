#!/usr/bin/python
# coding=UTF-8
'''
@Author: Recar
@Date: 2019-07-12 15:56:41
@LastEditTime: 2019-07-31 17:38:45
''' 

from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
from dns import resolver
from lib.log import logger
from scripts.port_masscan import PortMasscan
from scripts.port_nmap import PortNmap
from config.fingerprint import FINGERPRINTS
import re
import os
import subprocess
import requests
import json
import datetime

class WriteOutput(object):

    def __init__(
        self, domain=None, domains_file_path=None,
        webinfos_list=None, ip_port_names_list =None
        ):
        self.domain = domain
        self.domains_file_path = domains_file_path
        self.webinfos_list = webinfos_list
        self.ip_port_names_list  = ip_port_names_list 
        self.parsing_data()
        self.save()

    def parsing_data(self):
        self.result = list()
        """将两个结果信息结合到一起"""
        if self.webinfos_list and self.ip_port_names_list:
            for webinfo in self.webinfos_list:
                domain = webinfo["domain"]
                for ip_domain in self.ip_port_names_list:
                    if domain == ip_domain:
                        data = {
                            "webinfo":webinfo,
                            "ip_port_info": self.ip_port_names_list[domain]
                        }
                    self.result.append(data)
        elif self.webinfos_list and self.ip_port_names_list is None:
            for webinfo in self.webinfos_list:
                data = {
                        "webinfo":webinfo,
                        "ip_port_info": ""
                        }
                self.result.append(data)
        elif self.ip_port_names_list and self.webinfos_list is None:
                data = {
                        "webinfo":"",
                        "ip_port_info": self.ip_port_names_list
                        }
                self.result.append(data)

        
    def save(self):
        output = self.domain
        if self.domain is None:
            self.domain = output = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        base_path = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(base_path, "../", "output", output)
        output_path = f"{output_dir}/{self.domain}.json"
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)
        # print(self.result)
        with open(output_path, "w") as f:
            json.dump(self.result, f, indent=3, ensure_ascii=False)
        logger.info(f"save {self.domain} to {output_path}")


class PortScan(object):
    """对c段进行扫描 如果all_ports=True 使用masscan进行端口扫描后交给nmap进行服务识别              
        否则直接使用nmap进行常见端口扫描
        :param domain 测试的域名
        :param domains_file_path 测试的域名列表文件
        :param net_c: 是否对c段进行扫描  defalue=False
        :param all_ports: 是否对全端口进行扫描  defalue=False
        :param logger: 传入日志对象 不传入默认使用webfind自己的
        :return ip_port_names_list [ {domain: [ {ip:[{port: port, name: name}]},{ip:[{port: port, name: name}]} ], domain: []} ]
        usage:

        >>> ip_port_names_dict = PortScan(domain="www.test.com", net_c=True, all_ports=True).run()
    """
    def __init__(
        self, domain=None, domains_file_path=None,
        net_c=False, all_ports=False, logger=logger
        ):
        self.domains = list()
        # 指定的测试文件
        self.domains_file_path = domains_file_path
        # 处理下domain
        self.init_domains(domain)
        # 是否进行c段扫描
        self.net_c = net_c
        # 是否对全端口扫描
        self.all_ports = all_ports
        # 日志对象
        self.logger = logger
        # {domain: [ {ip:[{port: port, name: name}]},{ip:[{port: port, name: name}]} ], domain: []}
        self.domain_ip_port_names_dict = dict()

    def init_domains(self, domain):
        if self.domains_file_path:
            if os.path.exists(self.domains_file_path):
                with open(domains_file_path, "r") as f:
                    for domain in f:
                        self.domains.append(domain.split("    ")[0])
            else:
                self.logger.error("domains_file_path is not file")
        else:
            self.domains.append(domain)

    def is_alive(self, domain):
        """判断主机是否存活 使用ping的形式"""
        cmd = "ping -c 1 -w 1 {}".format(domain)
        # status = os.system(cmd)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True) 
        p.wait()
        status = p.returncode
        if status: #1 执行失败
            return False
        else:
            return True

    def domain_to_ip(self, domain):
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

    def run(self):
        logger.info("Port Scan")
        for domain in self.domains:
            self.logger.info(f"Target: {domain}")
            # 先判断是否存活
            alive = self.is_alive(domain)
            if not alive:
                self.logger.error(f"Not Alive: {domain}")
                continue
            # 将域名转为ip
            host = self.domain_to_ip(domain)
            if host:
                ip_port_names_list = list()
                # 如果进行C段扫描
                if self.net_c:
                    logger.info("C Segment Port Scan")
                    host = host+"/24"
                if self.all_ports:
                    # mas  先扫描一下存活的端口交给nmap再详细扫描
                    pmscan = PortMasscan(host, logger=self.logger)
                    host_open_port_list = pmscan.run()
                    for host_open_port in host_open_port_list:
                        host = host_open_port["host"]
                        open_ports = host_open_port["open_ports"]
                        # nmap 
                        pnscan = PortNmap(host, ports=open_ports, logger=self.logger)

                        ip_port_names_list.append(pnscan.run())
                    self.logger.info("port scan end")
                else:# 否则直接交给Nmap扫描 配置文件中的常见端口
                    pnscan = PortNmap(host, logger=self.logger)
                    ip_port_names_list = pnscan.run()
                    self.logger.info("Port Scan end")
                self.domain_ip_port_names_dict[domain] = ip_port_names_list
        return self.domain_ip_port_names_dict


class WebInfoScan():
    """获取指定域名的web信息
    :param domain  测试的域名
    :params domains_file_path 指定的domain测试文件的路径 
    :param logger 可选的传入日志对象控制日志输出
    :return webinfos 返回一个webinfo信息的列表 [{webinfo}, {webinfo}]

    weninfo = {
            "domain": "",
            "url": "",
            "title": "",
            "status_code": "",
            "server": "",
            "language": "",
            "framework":"",
            "headers": "",
            "body": "",
        }

    usage:

        >>> webinfos = WebInfoScan(domain="www.test.com").run()

    """
    def __init__(
        self, domain=None, domains_file_path=None,
        logger=logger
        ):
        self.domain = domain
        self.domains_file_path = domains_file_path
        self.logger = logger
        self.webinfos = list()

    def get_title(self, domain):
        """获取域名标题 server 语言信息"""
        target_url = domain
        if not domain.startswith("http"):
            target_url = f"http://{domain}"
        self.logger.info(f"Url: {target_url}")
        try:
            response = requests.get(target_url, timeout=3)
        except requests.exceptions.Timeout:
            return None
        except requests.exceptions.ConnectionError:
            return None
        # 状态码
        target_status_code = response.status_code
        self.logger.info(f"Status Code: {target_status_code}")
        # 服务器
        target_server = response.headers.get('Server')
        # 语言
        target_x_powered_by =  response.headers.get('X-Powered-By')
        if target_server:
            self.logger.info(f"Server: {target_server}")
        if target_x_powered_by:
            self.logger.info(f"X-Powered-By: {target_x_powered_by}")
        try:
            response_content = response.content.decode()
            # 标题
            target_title = re.findall('<title>([\s\S]*?)</title>', response_content)
            if target_title:
                for title in target_title:
                    if title:
                        target_title = title.strip()
                        self.logger.info(f"Title: {target_title}\n")
        except Exception:
            return None

        weninfo = {
            "domain": domain,
            "url": target_url,
            "title": target_title,
            "status_code": target_status_code,
            "server": target_server,
            "language": target_x_powered_by,
            "framework":"",
            "headers": response.headers,
            # "headers": "",
            "body": response.content.decode("utf-8")
            # "body": ""
        }
        return weninfo

    def get_web_framework(self, webinfo):
        """获取网站web框架"""
        # 先根据请求头里的信息来进行遍历获取
        self.logger.debug("simple discern web framework")
        targt_headers = webinfo["headers"]
        for key, value in targt_headers.items():
            # web 框架 指纹识别
            header_str = key+value
            for fingerprint in FINGERPRINTS.keys():
                if fingerprint in header_str:                    
                    self.logger.info("Web Framework: "+FINGERPRINTS[fingerprint])
                    webinfo["framework"] = FINGERPRINTS[fingerprint]
                    break
            # 要把headers转为dict因为 requests的headers类型是 CaseInsensitiveDict 不能直接json化
            webinfo["headers"] = dict(webinfo["headers"])
        self.webinfos.append(webinfo)

    def doamis_file_get_weninfo(self):
        """读取子域名的记录来解析"""
        domains = []
        if os.path.exists(self.domains_file_path):
            with open(self.domains_file_path, "r") as f:
                for domain_ips in f:
                    domains.append(domain_ips.split("    ")[0])
        return domains

    def run(self):
        domains = list()
        if self.domain:
            domains.append(self.domain)
        elif self.domains_file_path:
            domains = self.doamis_file_get_weninfo()
        # 获取webinfo
        for domain in domains:
            # 请求获取web信息
            webinfo = self.get_title(domain)
            # 简单的通过请求头来判断下web框架
            if webinfo:
                self.get_web_framework(webinfo)
        return self.webinfos
