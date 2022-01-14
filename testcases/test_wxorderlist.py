#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2022/1/6 17:08
# @File : test_wxorderlist.py
# @Project : PMS-API
import json
import unittest

from common.handleconf import conf
from common.handlelogs import log
from common.handlepath import DATADIR
from library.ddt import ddt, data
from common.handleexcel import ReadExcel
from common.handlerequest import SendRequest

cases_file = DATADIR + r"\apicases.xlsx"


@ddt
class WxorderList(unittest.TestCase):
    excel = ReadExcel(cases_file, "order_list")
    cases = excel.read_data()
    request = SendRequest()

    @classmethod
    def setUpClass(cls) -> None:
        token = conf.get("ilocation", "token")
        cls.token_value = token

    # def tearDown(self) -> None:
    #     pass

    @data(*cases)
    def test_wxorderlist(self, case):
        # 接口请求三部曲：url，头，体
        url = conf.get("ilocation", "url") + case["url"]
        method = case["method"]
        headers = eval(conf.get("evn", "headers"))
        headers["Authorization"] = self.token_value
        expected = int(case["status_code"])
        row = case["case_id"] + 1
        data = json.loads(case["data"])
        res = self.request.send(url=url, method=method, json=data, headers=headers)
        code = int(res.status_code)

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
