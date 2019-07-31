#!/usr/bin/python
# coding=UTF-8
'''
@Author: Recar
@Date: 2019-07-12 18:27:19
@LastEditTime: 2019-07-17 21:08:52
'''

from colorlog import ColoredFormatter
import logging

console_formatter = ColoredFormatter(
	"[%(asctime)s] %(log_color)s %(levelname)-5s%(reset)s %(white)s%(message)s",
	datefmt=None,
	reset=True,
	log_colors={
		'DEBUG':    'cyan',
		'INFO':     'green',
		'WARNING':  'yellow',
		'ERROR':    'red',
		'CRITICAL': 'red,bg_white',
	},
	secondary_log_colors={},
	style='%'
)

file_formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')
# 输出到控制台
console_handler = logging.StreamHandler()
console_handler.setFormatter(console_formatter)
# 输出到文件 mdoe=w 设置每次重新写入文件  
file_handler = logging.FileHandler('webfind.log', mode="w")
file_handler.setFormatter(file_formatter)
logger = logging.getLogger('webfind')
logger.addHandler(console_handler)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)
