#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/12/10 20:06
# @File : run_test.py
# @Project : PMS-API

import unittest
import os

from common.handleemail import send_email
from common.handlepath import CASEDIR, REPORTDIR
from library.HTMLTestRunnerNew import HTMLTestRunner

# 创建测试套件
suite = unittest.TestSuite()

# 加载测试用例到套件
loader = unittest.TestLoader()
suite.addTest(loader.discover(CASEDIR))

# 导入测试case
report_file = os.path.join(REPORTDIR, "report.html")

# 执行用例
runner = HTMLTestRunner(stream=open(report_file, "wb"),
                        description="接口测试报告",
                        title="PMS后台接口测试测试报告",
                        tester="谢光福"
                        )

runner.run(suite)

# 发送邮件
# send_email(report_file, "自动化测试报告")
