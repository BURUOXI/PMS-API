#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/12/13 15:49
# @File : handlerequest.py
# @Project : PMS-API

import requests


class SendRequest(object):
    """cookie+session鉴权的请求类封装"""

    def __init__(self):
        self.session = requests.session()

    def send(self, url, method, headers=None, params=None, data=None, json=None, files=None):
        global response
        method = method.lower()
        if method == "get":
            response = self.session.get(url=url, params=params, headers=headers)
        elif method == "put":
            response = self.session.put(url=url, data=data, headers=headers)
        elif method == "post":
            response = self.session.post(url=url, json=json, data=data, files=files, headers=headers)
        elif method == "patch":
            response = self.session.patch(url=url, json=json, data=data, files=files, headers=headers)
        elif method == "delete":
            response = self.session.delete(url=url, headers=headers)

        return response