#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2022/1/12 14:27
# @File : test_orders.py
# @Project : PMS-API

""" 运营后台订单管理 """

import json
import unittest
import requests
import jsonpath

from common.handleconf import conf
from common.handlelogs import log
from common.handlepath import DATADIR
from library.ddt import ddt, data
from common.handleexcel import ReadExcel
from common.handlerequest import SendRequest

cases_file = DATADIR + r"\apicases.xlsx"


@ddt
class OrderList(unittest.TestCase):
    excel = ReadExcel(cases_file, "htorder_list")
    cases = excel.read_data()
    request = SendRequest()

    @classmethod
    def setUpClass(cls) -> None:
        """ 登录获取token """
        # 1、准备登录的数据
        url = conf.get("evn", "url") + "/v1/property/user/login"
        data = {"mobile": eval(conf.get("test_data", "mobile")), "password": conf.get("test_data", "password")}
        headers = eval(conf.get("evn", "headers"))
        # 3、发送请求，进行登录
        response = cls.request.send(url=url, method="post", json=data, headers=headers)
        # 获取返回的数据
        res = response.json()
        # print(res)
        # 3、提取token,保存为类属性
        token = jsonpath.jsonpath(res, "token")[0]["access_token"]
        # token = jsonpath.jsonpath(res, "token")[0]
        # 将提取到的token设为类属性
        cls.token_value = "Bearer " + " " + token

    # def tearDown(self) -> None:
    #     pass

    @data(*cases)
    def test_orderlist(self, case):
        # 接口请求三部曲：url，头，体
        url = conf.get("evn", "url") + case["url"]
        method = case["method"]
        headers = eval(conf.get("evn", "headers"))
        headers["Company-Id"] = conf.get("evn", "Company-Id")
        headers["Authorization"] = self.token_value
        expected = int(case["status_code"])
        row = case["case_id"] + 1
        data = json.loads(case["data"])
        # data = {'type': 0, 'status': 'all', 'page': 3, 'page_size': 10}
        print(url, headers, method, data)
        res = self.request.send(url=url, method=method, params=data, headers=headers)
        code = int(res.status_code)
        print(code)

        if res.status_code == 201:

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

        else:
            result = res.text
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
    unittest.main()
