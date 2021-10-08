#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/21 下午3:28
# @Author  : lovemefan
# @File    : app.py
import os

from sanic import Sanic
import sys


from routes.ethereumRoute.ethereumRoute import ethereum_route

sys.path.append(os.path.abspath(os.pardir))


app = Sanic(__name__)


def load_banner():
    """load the banner"""
    with open('banner.txt', 'r', encoding='utf-8') as f:
        banner = f.read()

    print(banner)


app.blueprint(ethereum_route)

if __name__ == '__main__':
    load_banner()
    port = 8001
    app.run(host="0.0.0.0", port=port)

