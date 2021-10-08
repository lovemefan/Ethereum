#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/25 下午3:42
# @Author  : lovemefan
# @File    : UserRoute.py
import web3
from sanic import Blueprint, json

from model import ResponseBody
from service.ethereumApi import EthereumApi

ethereum_route = Blueprint('user', url_prefix='/api/user', version=1)
eth_api = EthereumApi()


@ethereum_route.route('/create_account', methods=['POST'])
async def create_account(request):
    """
    创建账号接口
    :param request:
    :return:
    """
    passphrase = request.json.get('passphrase', None)

    if passphrase is None:
        return json(ResponseBody(message="please input passphrase parameter"))
    else:
        result = eth_api.create_account(passphrase)
        return json(ResponseBody(message="SUCCESS", data=result))


@ethereum_route.route('/insert_file_and_key', methods=['POST'])
async def insert_file_and_key(request):
    """
    插入数据， 需要等待5秒
    :param request:
    :return:
    """
    address = request.json.get('address', None)
    file_name = request.json.get('file_name', None)
    encry_key = request.json.get('encry_key', None)
    passphrase = request.json.get('passphrase', None)

    if passphrase and address and file_name and encry_key is None:
        return json(ResponseBody(message="please make sure input all parameters"))
    else:
        result = eth_api.insert_file_and_key(address, file_name, encry_key, passphrase)
        return json(ResponseBody(message="SUCCESS", data=result))


@ethereum_route.route('/get_file_and_key', methods=['POST'])
async def get_file_and_key(request):
    """
    获取数据
    :param request:
    :return:
    """
    address = request.json.get('address', None)
    file_name = request.json.get('file_name', None)

    if address and file_name  is None:
        return json(ResponseBody(message="please make sure input all parameters"))
    else:
        result = eth_api.insert_file_and_key(address, file_name)
        return json(ResponseBody(message="SUCCESS", data=result))


@ethereum_route.route('/get_last_block', methods=['POST'])
async def get_last_block(request):
    """
    获取最后一块区块的信息
    :param request:
    :return:
    """
    result = eth_api.get_last_block()
    return json(ResponseBody(message="SUCCESS", data=result))


@ethereum_route.route('/get_block_number', methods=['POST'])
async def get_block_number(request):
    """
    获取区块的数量
    :param request:
    :return:
    """
    result = eth_api.get_block_number()
    return json(ResponseBody(message="SUCCESS", data=result))


@ethereum_route.route('/get_block', methods=['POST'])
async def get_block(request):
    """
    获取某一块区块的信息
    :param request:
    :return:
    """
    index = int(request.json.get('index', 0))
    result = eth_api.get_block(index)
    return json(ResponseBody(message="SUCCESS", data=result))


@ethereum_route.route('/unlock_account', methods=['POST'])
async def unlock_account(request):
    """
    给某一个用户解锁
    :param request:
    :return:
    """
    address = request.json.get('address', None)
    passphrase = request.json.get('passphrase', None)
    duration = request.json.get('duration', None)
    duration = duration and int(duration)
    if address and passphrase is None:
        return json(ResponseBody(message="please make sure input all parameters"))

    result = eth_api.unlock_account(address, passphrase, duration)
    return json(ResponseBody(message="SUCCESS", data=result))


@ethereum_route.route('/start_mining', methods=['POST'])
async def start_mining(request):
    """
    获取区块的数量
    :param request:
    :return:
    """
    address = request.json.get('address', None)
    thread_count = request.json.get('thread_count', None)
    thread_count = thread_count and int(thread_count)

    if address and thread_count is None:
        return json(ResponseBody(message="please make sure input all parameters"))

    result = eth_api.start_mining(address, thread_count)
    return json(ResponseBody(message="SUCCESS", data=result))


@ethereum_route.exception(web3.exceptions.InvalidAddress)
async def invalid_address(request, exception):
    response = ResponseBody(
        message="ERROR, address is not exist",
        code=400
    )
    return json(response.__dict__(), 400)


@ethereum_route.exception(web3.exceptions.ContractLogicError)
async def contract_logic_error(request, exception):
    response = ResponseBody(
        message=f"ERROR, {str(exception)}",
        code=400
    )
    return json(response.__dict__(), 400)


@ethereum_route.exception(web3.exceptions.BlockNotFound)
async def block_not_found(request, exception):
    response = ResponseBody(
        message=f"ERROR, Block Not Found",
        code=400
    )
    return json(response.__dict__(), 400)







