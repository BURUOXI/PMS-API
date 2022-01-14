#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/12/30 15:19
# @File : handbasedata.py
# @Project : PMS-API
import jsonpath

from common.handleconf import conf
from common.handlerequest import SendRequest

class BaseData(object):

    request = SendRequest()

    """
    1.获取登录账号的公司id
    2.获取改账号公司id下的展位id值
    3.将两个id最后一个值存入cong存储
    """
    @classmethod
    def login(cls):
        """登录获取token"""
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
        company_id = jsonpath.jsonpath(res, "user")[0]["company_id"]
        conf.write_data("evn", "Company-Id", str(company_id))


    def getshops(self):
        url = conf.get("evn", "url") + "/v1/property/shops/list"
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
        print(shops_id)
        conf.write_data("evn", "shops_id", str(shops_id))



if __name__ == '__main__':
    A = BaseData()
    A.login()
    A.getshops()
