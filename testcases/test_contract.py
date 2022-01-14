#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/12/30 14:21
# @File : test_contract.py
# @Project : PMS-API
import datetime
import json
import unittest
import random

import jsonpath

from common.handleconf import conf
from common.handlelogs import log
from common.handlerandom import chinese_name, random_company, random_phone_number, start_data, date_now
from library.ddt import ddt, data
from common.handlerequest import SendRequest
from common.handleexcel import ReadExcel
from common.handlepath import DATADIR

cases_file = DATADIR + r"\apicases.xlsx"



@ddt
class TestContract(unittest.TestCase):
    excel = ReadExcel(cases_file, "contract")
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
        # 3、提取token,保存为类属性
        token = jsonpath.jsonpath(res, "token")[0]["access_token"]
        # token = jsonpath.jsonpath(res, "token")[0]
        # 将提取到的token设为类属性
        cls.token_value = "Bearer " + " " + token

    @classmethod
    def tearDown(self) -> None:
        pass

    @data(*cases)
    def test_contract(self, case):
        # 接口请求三部曲：url，头，体

        url = conf.get("evn", "url") + case["url"]
        method = case["method"]
        headers = eval(conf.get("evn", "headers"))
        headers["Company-Id"] = conf.get("evn", "Company-Id")
        headers["Authorization"] = self.token_value

        # 随机生成合同名
        contract_name = "自动测试合同-" + str(random.randint(0, 100))
        case["data"] = case["data"].replace("#name#", contract_name)

        # 随机生成公司名称
        company = random_company()
        case["data"] = case["data"].replace("#merchant#", company)

        # 随机生成客户名称
        customer_name = chinese_name().replace(" ", "")
        case["data"] = case["data"].replace("#merchant_contact#", customer_name)

        # 随机生成手机号
        phone_number = random_phone_number()
        case["data"] = case["data"].replace("#contact_mobile#", phone_number)

        # 随机生成订单开始时间和结束时间（开始时间为明天）
        star_data = (date_now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        end_data = (datetime.datetime.now() + datetime.timedelta(days=5)).strftime('%Y-%m-%d')
        case["data"] = case["data"].replace("#star_data#", star_data)
        case["data"] = case["data"].replace("#end_data#", end_data)

        # 获取期望值
        expected = int(case["status_code"])
        row = case["case_id"] + 1
        data = json.loads(case["data"])

        res = self.request.send(url=url, method=method, json=data, headers=headers)
        code = int(res.status_code)
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
