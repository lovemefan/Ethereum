# -*- coding: utf-8 -*-
# @Time  : 2021/9/20 16:51
# @Author : lovemefan
# @Email : lovemefan@outlook.com
# @File : ethereumApi.py
import json
import time
import traceback

import web3
from web3 import Web3

from service.singleton import Singleton


@Singleton
class EthereumApi(object):

    def __init__(self, default_account=None):
        self._w3 = Web3(Web3.HTTPProvider('http://222.197.219.26:8545'))
        with open("../sol/corpus.abi") as file:
            self._abi = json.loads(file.read())
        # 合约账户节点
        self._default_account = default_account or self._w3.eth.accounts[1]
        self._contract_address = "0xd35186CD127732BB876A634CF5f98F4ef121aA65"
        self._contract = self._w3.eth.contract(self._contract_address, abi=self._abi)

    def create_account(self, passphrase: str):
        """
        创建一个账户
        :param passphrase: 相当于密码
        :return: 返回一个账户地址
        """
        account = self._w3.geth.personal.newAccount(passphrase)
        # 顺便解锁该账号
        self._w3.geth.personal.unlock_account(account, passphrase)
        return account

    def contract_call(self, meth_name: str, *args, **kwargs):
        """
        调用合约中的方法
        :param meth_name:
        :return:
        """
        return eval(f"self._contract.functions.{meth_name}().call(*args, **kwargs)")

    def get_balances(self, address):
        """
        获取当前账户合约中的余额
        :param address:
        :return:
        """
        return self._contract.caller({'from': address}).getBalances()

    def insert_file_and_key(self, address: str, file_name, encry_key):
        """
        向链中插入数据， 其中每个地址为一个用户，为该用户插入一条数据，数据为对应file的加密key
        :param address: 用户地址
        :param file_name: 文件名
        :param encry_key: 加密字符串
        :return: boolean 返回是否执行成功
        :exception
        """
        return self._contract.caller({'from': address}).insertFileKey(address, file_name, encry_key)

    def get_file_and_key(self, address: str, file_name):
        """
        获取某个用户的文件的密钥
        :param address: 用户地址
        :param file_name: 文件名
        :return: 返回密钥
        """
        return self._contract.caller({'from': address}).getFileKey(address, file_name)

    def get_last_block(self):
        """
        获取最后一个区块
        :return:
        """
        return dict(self._w3.eth.get_block('latest'))

    def get_block_number(self):
        """
        获取区块数量
        :return:
        """
        return self._w3.eth.block_number

    def get_block(self,  index: int):
        """
        获取第index的区块
        :param index:区块下标
        :return:
        """
        return self._w3.eth.get_block(index)

    def start_mining(self, address: str, thread_count=1):
        """
        开始挖矿
        :param thread_count: 启动挖矿的线程数，为了不影响性能，默认为1
        :param address:
        :return:
        """
        self._w3.geth.miner.set_etherbase(address)
        # 挖5秒的矿
        self._w3.geth.miner.start(thread_count)
        time.sleep(5)
        self._w3.geth.miner.stop()



if __name__ == '__main__':
    my_account = "0xa09c6E4A292fa10879cb9d3B0560eDedd7aD7488"

    try:
        my_eth = EthereumApi()
        print(my_eth._w3.eth.accounts)
        message = my_eth.insert_file_and_key(my_account, "test1.jpg", "abcd12345678")
        print(message)

        print(my_eth._w3.eth.get_balance(my_account))
        my_eth.start_mining(my_account)
        print(my_eth._w3.eth.get_balance(my_account))

        key = my_eth.get_file_and_key("0xa09c6E4A292fa10879cb9d3B0560eDedd7aD7488", "test.jpg")
        print(key)
        print(my_eth.get_last_block())
        print(my_eth.get_block_number())
        print(my_eth.get_block(20))
    except web3.exceptions.InvalidAddress as e1:
        # 地址非法
        traceback.print_exc()
        print(e1)
    except web3.exceptions.ContractLogicError as e2:
        # 传入图片名不存在等合约错误
        traceback.print_exc()
        print(e2)
    except web3.exceptions.BlockNotFound as e3:
        # 区块不存
        traceback.print_exc()
        print(e3)