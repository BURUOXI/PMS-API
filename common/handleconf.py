#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/12/13 14:16
# @File : handleconf.py
# @Project : PMS-API


import os
from configparser import ConfigParser
from common.handlepath import CONFDIR


class HandleConfig(ConfigParser):

    def __init__(self, filename):
        # 调用父类的init方法
        super().__init__()
        self.filename = filename
        self.read(filename,encoding="utf8")

    def write_data(self, section, options, value):
        """写入数据的方法"""
        self.set(section, options, value)
        self.write(fp=open(self.filename, "w"))


conf = HandleConfig(os.path.join(CONFDIR, "config.ini"))
