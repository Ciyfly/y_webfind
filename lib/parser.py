#!/usr/bin/python
# coding=UTF-8
'''
@Author: Recar
@Date: 2019-07-12 15:31:40
@LastEditTime: 2019-07-12 15:51:45
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
    
    parser.add_option('--json',action='store_true', dest="is_json", default=False, help="是否生成json报告")

    parser.add_option('--html',action='store_true', dest="is_html", default=False, help="是否生成html报告")
    (options,args) = parser.parse_args()
    if  options.target==None:
        parser.print_help()
        sys.exit(0)
    if "www" in options.target or "http://" in options.target :
        options.target =options.target.replace("www.","").replace("http://", "")
    if options.engine:
        options.engine = options.engine.split(",")
    return options