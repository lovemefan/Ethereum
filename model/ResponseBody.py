#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/25 下午9:49
# @Author  : lovemefan
# @File    : ResponseBody.py
import json


class ResponseBody(object):
    """The response body of http"""

    def __init__(self, message='', data='', code=200):
        self.message = message
        self.data = data
        self.code = code

    def to_json_string(self):
        return json.dumps(self.__dict__).encode('utf-8')
