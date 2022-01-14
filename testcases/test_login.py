#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/12/11 13:40
# @File : test_login.py
# @Project : PMS-API

"""使用requests模块发送请求"""
from common.handleexcel import ReadExcel
from common.handleconf import conf
from common.handlepath import DATADIR
from common.handlerequest import SendRequest
from common.handlelogs import log

import unittest
from library.ddt import ddt, data

case_file = DATADIR+ r"\apicases.xlsx"


@ddt
class TestLogin(unittest.TestCase):
    excel = ReadExcel(case_file, "login")
    cases = excel.read_data()
    request =SendRequest()

    @data(*cases)
    def test_login(self, case):
        # 接口请求三部曲：url，头，体
        url = conf.get("evn", "url") + case["url"]
        method = case["method"]
        # print(type(method))
        headers = {"Content-Type": "application/json"}

        data = eval(case["data"])
        expected = int(case["status_code"])
        row = case["case_id"] + 1
        res = self.request.send(url=url, method=method, json=data, headers=headers)
        code = int(res.status_code)
        print(res.json())  # 获取返回参数

        # print(case["status_code"])
        # print(res.status_code)
        # print(res.status_code)  #使用code码断言

        # 断言
        try:
            self.assertEqual(expected, code)
            # self.assertEqual(expected["msg"], res["msg"])

        except AssertionError as e:
            self.excel.write_data(row=row, column=8, value="未通过")
            log.error("用例：{}，执行未通过".format(case["title"]))
            log.exception(e)
            raise e
        else:
            self.excel.write_data(row=row, column=8, value="通过")
            log.info("用例：{}，执行通过".format(case["title"]))


if __name__ == '__main__':
    unittest.main()  # 测试当前函数是否正常
