# -*- coding: utf-8 -*-
# @Time  : 2021/9/20 16:51
# @Author : lovemefan
# @Email : lovemefan@outlook.com
# @File : ethereumApi.py
import json

from web3 import Web3

from service.singleton import Singleton


@Singleton
class EthereumApi(object):

    def __init__(self):
        self.__w3 = Web3(Web3.HTTPProvider('http://222.197.219.26:8545'))
        with open("../sol/corpus.abi") as file:
            self.__abi = json.loads(file.read())
        # 合约账户节点
        self.__default_account = self.__w3.eth.accounts[1]
        self.__contract = self.__w3.eth.contract(self.__default_account, abi=self.__abi)

    def create_account(self):
        pass

    def contract_call(self, meth_name: str, *args, **kwargs):
        """
        调用合约中的方法
        :param meth_name:
        :return:
        """
        return eval(f"self.__contract.functions.{meth_name}().call(*args, **kwargs)")


if __name__ == '__main__':
    eth = EthereumApi()
