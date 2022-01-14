#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/12/21 11:46
# @File : handlecitydata.py
# @Project : PMS-API
import json

import jsonpath
import requests
from common.handleconf import conf
from common.handlerequest import SendRequest

class CityData(object):
    request = SendRequest()

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

    def get_linhuibooth(self):
        """调用邻汇吧后台城市列表接口"""
        url = conf.get("evn", "url") + "/api/city"
        headers = {"Content-Type": "application/json", "x-client": "bc", "x-client-version": "3.27"}
        res = requests.get(url=url, headers=headers).json()
        re = json.loads(res)
        print(re)

if __name__ == '__main__':
    CityData().get_linhuibooth()