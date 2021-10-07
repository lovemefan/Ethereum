#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/25 下午3:42
# @Author  : lovemefan
# @File    : UserRoute.py
from sanic import Blueprint

user_route = Blueprint('user', url_prefix='/api/user', version=1)


@user_route.route('/validate_password', methods=['POST'])
async def create_account(request):
    username = request.json.get('username', None)
    password = request.json.get('password', None)
