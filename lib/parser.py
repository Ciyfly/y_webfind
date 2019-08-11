#!/usr/bin/python
# coding=UTF-8
'''
@Author: Recar
@Date: 2019-07-12 15:31:40
@LastEditTime: 2019-08-09 19:19:27
'''

from optparse import OptionParser
from config.config import VERSION, BANNER
USAGE = "python -d www.xxx.com --netc --ap --debug --json"
import sys
def get_options():
    print(BANNER)
    parser = OptionParser(usage=USAGE, version=VERSION)

    parser.add_option('-d', type=str, dest="domain", help="指定测试的域名")
    
    parser.add_option('-f', type=str, dest="domains_file_path", help="指定子域名的txt结果/ 域名列表文件")

    parser.add_option('--web',action='store_true', dest="webinfo", default=False, help="是否获取web网站信息")

    parser.add_option('--port',action='store_true', dest="port_scan", default=False, help="是否进行端口扫描")
    
    parser.add_option('--netc',action='store_true', dest="net_c", default=False, help="是否对c段进行扫描")

    parser.add_option('--ap',action='store_true', dest="all_ports", default=False, help="是否对全端口进行扫描 默认只进行常见端口")

    parser.add_option('--weak',action='store_true', dest="weak_scan", default=False, help="是否对识别的服务进行弱口令扫描")
    
    parser.add_option('--debug',action='store_true', dest="debug", default=False, help="设置日志输出的级别输出debug日志")

    # parser.add_option('--json',action='store_true', dest="is_json", default=False, help="是否生成json报告")

    # parser.add_option('--html',action='store_true', dest="is_html", default=False, help="是否生成html报告")
    (options,args) = parser.parse_args()
    if  options.domain==None and options.domains_file_path==None:
        parser.print_help()
        sys.exit(0)
    return options