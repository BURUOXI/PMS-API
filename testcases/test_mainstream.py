#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/12/22 11:27
# @File : test_mainstream.py
# @Project : PMS-API

""" 主流程 """
import json
import random
import unittest

import jsonpath

from common.handleconf import conf
from common.handlelogs import log
from common.handlerequest import SendRequest
from common.handlepath import DATADIR
from common.handleexcel import ReadExcel
from library.ddt import ddt, data

cases_file = DATADIR + r"\apicases.xlsx"

@ddt
class MainStream(unittest.TestCase):
    request = SendRequest()
    excel = ReadExcel(cases_file, "main_stream")
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

    @data(*cases)
    def test_mainstream(self, case):


        # 接口请求三部曲：url，头，体
        url = conf.get("evn", "url") + case["url"]
        method = case["method"]
        headers = eval(conf.get("evn", "headers"))
        headers["Company-Id"] = conf.get("evn", "Company-Id")
        headers["Authorization"] = self.token_value
        case_name = "自动化展位 " + str(random.randint(10, 100))
        case["data"] = case["data"].replace("#name#", case_name)
        expected = int(case["status_code"])
        row = case["case_id"] + 1

        # res = self.request.send(url=url, method=method, json=data, headers=headers)
        # code = int(res.status_code)
        if case["method"] == "get":
            data = json.loads(case["data"])
            res = self.request.send(url=url, method=method, json=data, headers=headers)
            res_data = jsonpath.jsonpath(res.json(), "data")
            shop_id = []
            for i in res_data[0]:
                shop_id.append(i["id"])

            self.excel.write_data(row=row + 1, column=5, value=shop_id[0])

        elif case["method"] == "delete":
            data = json.loads(case["data"])
            try:
                res_url = url + "/" + str(case["list_id"]+1)        # case读取时候没有获取到当前获取列表的数据，读的是上次的id

                res = self.request.send(url=res_url, method=method, json=data, headers=headers)
                code = int(res.status_code)
                result = res.text
                try:
                    self.assertEqual(expected, code)
                    # self.assertEqual(expected["msg"], res["msg"])
                except AssertionError as e:
                    self.excel.write_data(row=row, column=9, value="未通过")
                    log.error("用例：{}，执行未通过".format(case["title"]))
                    log.exception(e)
                    raise e
                else:
                    self.excel.write_data(row=row, column=9, value="通过")
                    log.info("用例：{}，执行通过".format(case["title"]))
            except AssertionError as e:
                log.error("{}id查询为空".format(case["title"]))
                log.exception(e)
                raise e
        elif case["method"] == "post" and case["list_id"] != None:
            da = {}  # 广告位的删除接口不规范导致需要特殊处理
            da["ids"] = [case["list_id"]]
            case["data"] = da
            data = case["data"]
            res = self.request.send(url=url, method=method, json=data, headers=headers)
            code = int(res.status_code)
            try:
                self.assertEqual(expected, code)
                # self.assertEqual(expected["msg"], res["msg"])
            except AssertionError as e:
                self.excel.write_data(row=row, column=9, value="未通过")
                log.error("用例：{}，执行未通过".format(case["title"]))
                log.exception(e)
                raise e
            else:
                self.excel.write_data(row=row, column=9, value="通过")
                log.info("用例：{}，执行通过".format(case["title"]))
        else:
            data = json.loads(case["data"])
            res = self.request.send(url=url, method=method, json=data, headers=headers)
            code = int(res.status_code)
            if res.status_code == 201:
                # 断言
                try:
                    self.assertEqual(expected, code)
                    # self.assertEqual(expected["msg"], res["msg"])
                except AssertionError as e:
                    self.excel.write_data(row=row, column=9, value="未通过")
                    log.error("用例：{}，执行未通过".format(case["title"]))
                    log.exception(e)
                    raise e
                else:
                    self.excel.write_data(row=row, column=9, value="通过")
                    log.info("用例：{}，执行通过".format(case["title"]))

            else:
                result = res.text
                # 断言
                try:
                    self.assertEqual(expected, code)
                    # self.assertEqual(expected["msg"], res["msg"])

                except AssertionError as e:
                    self.excel.write_data(row=row, column=9, value="未通过")
                    log.error("用例：{}，执行未通过".format(case["title"]))
                    log.exception(e)
                    raise e
                else:
                    self.excel.write_data(row=row, column=9, value="通过")
                    log.info("用例：{}，执行通过".format(case["title"]))


if __name__ == '__main__':
    unittest.main()
