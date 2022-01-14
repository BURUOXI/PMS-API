#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/12/14 20:22
# @File : test_shop.py
# @Project : PMS-API

"""使用requests模块发送请求"""
import json
import unittest

import jsonpath


from common.handleexcel import ReadExcel
from common.handleconf import conf
from common.handlepath import DATADIR
from common.handlerandom import random_name, chinese_name
from common.handlerequest import SendRequest
from common.handlelogs import log
from library.ddt import ddt, data

case_file = DATADIR + r"\apicases.xlsx"

@ddt
class TestShop(unittest.TestCase):
    excel = ReadExcel(case_file, "shop")
    cases = excel.read_data()
    request =SendRequest()

    # def setUp(self):
    #     pass

    @classmethod
    def setUpClass(cls):
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
        # 获取当前用户的公司id  ------要不要后面看需求再补。先在配置文件写死掉

        # # 第一次获取项目列表id
        # shopid1 = TestShop().getshoplist()
        # print(shopid1)
        # return shopid1




    # def test_getshoplist(self):
    def getshoplist(self):
        url = conf.get("evn", "url") + "/v1/property/shops/list"
        # data = {"mobile": eval(conf.get("test_data", "mobile")), "password": conf.get("test_data", "password")}
        headers = eval(conf.get("evn", "headers"))
        headers["Company-Id"] = conf.get("evn", "Company-Id")
        headers["Authorization"] = self.token_value
        # 3、发送请求，进行登录
        response = self.request.send(url=url, method="get", headers=headers)
        data = response.json()
        shops_id = []
        shop_id = jsonpath.jsonpath(data, "data")
        for i in shop_id[0]:
            shops_id.append(i["id"])

        return shops_id

    @classmethod
    def tearDownClass(cls):
        # 获取项目列表数据第二次
        shopid2 = TestShop().getshoplist()
        # 1、准备删除url的数据
        url = conf.get("evn", "url") + "/v1/property/shops/" + str(shopid2[0])
        headers = eval(conf.get("evn", "headers"))
        headers["Company-Id"] = conf.get("evn", "Company-Id")
        headers["Authorization"] = cls.token_value
        # 3、发送请求，进行删除
        response = cls.request.send(url=url, method="delete", headers=headers)

    @data(* cases)
    def test_addShop(self, case):

        # 接口请求三部曲：url，头，体
        url = conf.get("evn", "url") + case["url"]
        method = case["method"]
        headers = eval(conf.get("evn", "headers"))
        headers["Company-Id"] = conf.get("evn", "Company-Id")
        headers["Authorization"] = self.token_value
        # 随机生成项目名
        name = chinese_name().replace(" ", "")
        case["data"] = case["data"].replace("#name#", name)
        expected = case["status_code"]
        row = case["case_id"] + 1
        data = json.loads(case["data"])

        res = self.request.send(url=url, method=method, json=data, headers=headers)

        if res.status_code == 201:

            # 断言
            try:
                self.assertEqual(expected, str(res.status_code))
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
                self.assertEqual(expected, res.status_code)
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

