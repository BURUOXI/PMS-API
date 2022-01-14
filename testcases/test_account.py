#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/12/17 11:53
# @File : test_account.py
# @Project : PMS-API
import json
import unittest

import jsonpath

from common.handleconf import conf
from common.handlelogs import log
from common.handlepath import DATADIR
from common.handlerandom import chinese_name, credit_card_number
from common.handlerequest import SendRequest
from common.handleexcel import ReadExcel
from library.ddt import ddt, data

case_file = DATADIR + r"\apicases.xlsx"




@ddt
class TestAccount(unittest.TestCase):
    request = SendRequest()
    excel = ReadExcel(case_file, "account")
    cases = excel.read_data()

    @classmethod
    def setUpClass(cls) -> None:
        """登录获取token"""
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

    @classmethod
    def tearDownClass(cls) -> None:
        """测试用例执行完，清除脏数据"""
        # 获取项目列表数据第二次
        accountid2 = TestAccount().test_getaccountlist()

        for id in accountid2[0:-1]:

            # 1、准备删除url的数据
            url = conf.get("evn", "url") + "/v1/property/beneficiary_accounts/" + str(id)
            headers = eval(conf.get("evn", "headers"))
            headers["Company-Id"] = conf.get("evn", "Company-Id")
            headers["Authorization"] = cls.token_value
            # 3、发送请求，进行删除
            response = cls.request.send(url=url, method="delete", headers=headers)

    def test_getaccountlist(self):
        url = conf.get("evn", "url") + "/v1/property/beneficiary_accounts"
        # data = {"mobile": eval(conf.get("test_data", "mobile")), "password": conf.get("test_data", "password")}
        headers = eval(conf.get("evn", "headers"))
        headers["Company-Id"] = conf.get("evn", "Company-Id")
        headers["Authorization"] = self.token_value
        # 3、发送请求，进行登录
        response = self.request.send(url=url, method="get", headers=headers)
        data = response.json()
        account_ids = []    # 创建一个新列表，将获取到的id装进来

        account_id = jsonpath.jsonpath(data, "data")    # 处理接口获取到的id
        for i in account_id[0]:
            account_ids.append(i["id"])

        return account_ids  # 将返回的id已列表返回

    @data(*cases)
    def test_account(self, case):
        # 接口请求三部曲：url，头，体
        url = conf.get("evn", "url") + case["url"]
        method = case["method"]
        headers = eval(conf.get("evn", "headers"))
        headers["Company-Id"] = conf.get("evn", "Company-Id")
        headers["Authorization"] = self.token_value
        # 随机生成项目名
        name = chinese_name().replace(" ", "")

        care_id = credit_card_number()

        case["data"] = case["data"].replace("#name#", name)
        case["data"] = case["data"].replace("#cara_id#", care_id)
        # print(case)
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
    unittest.main()  # 测试当前函数是否正常
