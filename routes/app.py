#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/21 下午3:28
# @Author  : lovemefan
# @File    : app.py
import os
import sys
sys.path.append(os.path.abspath(os.getcwd()))
print(os.path.abspath(os.getcwd()))
from model.ResponseBody import ResponseBody
from sanic import Sanic, json
import sys


from routes.ethereumRoute.ethereumRoute import ethereum_route, eth_api

sys.path.append(os.path.abspath(os.pardir))


app = Sanic(__name__)

@app.route('/v1/api/user/start_mining', methods=['POST'])
async def start_mining(request):
    """
    挖矿
    :param request:
    :return:
    """
    address = request.json.get('address', None)
    thread_count = request.json.get('thread_count', 1)
    duration = request.json.get('duration', 5)
    thread_count = min(thread_count and int(thread_count), 10)
    duration = min(duration and int(duration), 60)

    if address and thread_count is None:
        return json(ResponseBody(message="please make sure input all parameters").__dict__)
    app.add_task(eth_api.start_mining(address, thread_count, duration))
    return json(ResponseBody(message="SUCCESS", data="").__dict__)


def load_banner():
    """load the banner"""
    with open('routes/banner.txt', 'r', encoding='utf-8') as f:
        banner = f.read()

    print(banner)


app.blueprint(ethereum_route)

if __name__ == '__main__':
    load_banner()
    port = 8001
    app.run(host="0.0.0.0", port=port)

