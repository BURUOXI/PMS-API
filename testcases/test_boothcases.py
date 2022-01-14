#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2022/1/4 17:35
# @File : test_boothcases.py
# @Project : PMS-API
import json
import random
import unittest

import jsonpath

from common.handleconf import conf
from common.handleexcel import ReadExcel
from common.handlelogs import log
from common.handlepath import DATADIR
from common.handlerandom import set_random_pyint
from common.handlerequest import SendRequest
from ddt import ddt, data
case_file = DATADIR + r"\apicases.xlsx"


@ddt
class TestBoothcases(unittest.TestCase):
    excel = ReadExcel(case_file, "boothcases")
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

    @data(*cases)
    def testboothcases(self, case):
        # 接口请求三部曲：url，头，体
        url = conf.get("evn", "url") + case["url"]
        method = case["method"]
        headers = eval(conf.get("evn", "headers"))
        headers["Company-Id"] = conf.get("evn", "Company-Id")
        headers["Authorization"] = self.token_value

        # 随机生成展位编号名
        num = set_random_pyint(1, 500)
        booth_num = "PMS " + str(num)
        case["data"] = case["data"].replace("#num#", booth_num)

        # 随机生成展位名
        booth_name = "PMS自动测试展位-" + "佛山海琴水岸" + str(random.randint(0, 100))
        case["data"] = case["data"].replace("#name#", booth_name)
        print(booth_name)

        expected = int(case["status_code"])
        row = case["case_id"] + 1
        data = json.loads(case["data"])

        res = self.request.send(url=url, method=method, json=data, headers=headers)
        code = int(res.status_code)

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
