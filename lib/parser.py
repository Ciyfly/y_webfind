#!/usr/bin/python
# coding=UTF-8
'''
@Author: Recar
@Date: 2019-07-12 15:31:40
@LastEditTime: 2019-07-17 21:52:09
'''

from optparse import OptionParser
from config.config import VERSION, BANNER
USAGE = "python -t www.xxx.com"
import sys
def get_options():
    print(BANNER)
    parser = OptionParser(usage=USAGE, version=VERSION)

    parser.add_option('-t', type=str, dest="target", help="指定要测试的域名或者ip")
    
    parser.add_option('-e', type=str, dest="engine", help="指定使用的引擎 逗号间隔")
    
    parser.add_option('-l', type=str, dest="domain_log_path", help="指定子域名的txt结果")
    
    parser.add_option('-d', type=str, dest="domain", help="指定测试的主域名 用于保存结果 不指定则使用时间戳")

    parser.add_option('--netc',action='store_true', dest="net_c", default=False, help="是否对c段进行扫描")

    parser.add_option('--ap',action='store_true', dest="all_ports", default=False, help="是否对全端口进行扫描 默认只进行常见端口")
    
    parser.add_option('--debug',action='store_true', dest="debug", default=False, help="设置日志输出的级别输出debug日志")

    parser.add_option('--json',action='store_true', dest="is_json", default=False, help="是否生成json报告")

    parser.add_option('--html',action='store_true', dest="is_html", default=False, help="是否生成html报告")
    (options,args) = parser.parse_args()
    if  options.target==None and options.domain_log_path==None:
        parser.print_help()
        sys.exit(0)
    if options.target:
        if "www" in options.target or "http://" in options.target :
            options.target =options.target.replace("www.","").replace("http://", "")
    if options.engine:
        options.engine = options.engine.split(",")  
    return options