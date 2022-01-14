#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2022/1/7 16:34
# @File : test_Wxorder.py
# @Project : PMS-API

"""微信小程序下单操作
1.获取展位信息----配置文件获取


"""
import datetime
import json
import unittest

from common.handleconf import conf
from common.handlelogs import log
from common.handlepath import DATADIR
from common.handlerandom import date_now
from library.ddt import ddt, data
from common.handleexcel import ReadExcel
from common.handlerequest import SendRequest

cases_file = DATADIR + r"\apicases.xlsx"


@ddt
class WxOrder(unittest.TestCase):
    excel = ReadExcel(cases_file, "Wxorder")
    cases = excel.read_data()
    request = SendRequest()

    @classmethod
    def setUpClass(cls) -> None:
        token = conf.get("ilocation", "token")
        cls.token_value = token

    # def tearDown(self) -> None:
    #     pass

    @data(*cases)
    def test_wxorder(self, case):
        # 接口请求三部曲：url，头，体
        booth_id = conf.get("ilocation", "id")
        case["url"] = case["url"].replace("{id}", booth_id)
        url = conf.get("ilocation", "url") + case["url"]

        method = case["method"]
        headers = eval(conf.get("evn", "headers"))
        headers["Authorization"] = self.token_value
        #
        star_data = (date_now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        end_data = (datetime.datetime.now() + datetime.timedelta(days=5)).strftime('%Y-%m-%d')
        case["data"] = case["data"].replace("#star_data#", star_data)
        case["data"] = case["data"].replace("#end_data#", end_data)


        expected = int(case["status_code"])
        row = case["case_id"] + 1
        data = json.loads(case["data"])
        print(url, method, data, headers)
        res = self.request.send(url=url, method=method, data=data, headers=headers)
        print(res.json())
        code = int(res.status_code)
        print(code)

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




