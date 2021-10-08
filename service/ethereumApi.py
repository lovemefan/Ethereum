# -*- coding: utf-8 -*-
# @Time  : 2021/9/20 16:51
# @Author : lovemefan
# @Email : lovemefan@outlook.com
# @File : ethereumApi.py
import json
import threading
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
        self._contract_address = "0xF4a45BE0272e903Ef45b33e2F823ed846f4B600E"
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

    def insert_file_and_key(self, address: str, file_name: str, encry_key: str, passphrase: str):
        """
        向链中插入数据， 其中每个地址为一个用户，为该用户插入一条数据，数据为对应file的加密key
        :param address: 用户地址
        :param file_name: 文件名
        :param encry_key: 加密字符串
        :param passphrase: 账户密码，用户解锁才可以交易
        :return: boolean 返回是否执行成功
        :exception
        """
        self.unlock_account(address, passphrase=passphrase, duration=10)
        tx_hash = self._contract.functions.insertFileKey(address, file_name, encry_key).transact({'from': address})
        # 开始挖矿
        threading.Thread(target=self.start_mining(address)).start()
        tx_receipt = self._w3.eth.wait_for_transaction_receipt(tx_hash)

        return tx_receipt

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

    def unlock_account(self, address, passphrase, duration=None):
        """
        解锁某一账户，进行交易
        :param duration: 持续时间，None为永久解锁
        :param address: 账户地址
        :param passphrase: 账户密码
        :return: bool 是否执行成功
        """
        return self._w3.parity.personal.unlock_account(address, passphrase, duration)


if __name__ == '__main__':
    my_account = "0xa09c6E4A292fa10879cb9d3B0560eDedd7aD7488"

    try:
        my_eth = EthereumApi()
        print(my_eth._w3.eth.accounts)
        message = my_eth.insert_file_and_key(my_account, "test4.jpg", "abcd12345678abc43", "Tz973158")
        # print(str(message))

        # print(my_eth._w3.eth.get_balance(my_account))
        # my_eth.start_mining(my_account)
        # print(my_eth._w3.eth.get_balance(my_account))

        key = my_eth.get_file_and_key(my_account, "test4.jpg")
        print(key)

        # print(my_eth.get_last_block())
        # print(my_eth.get_block_number())
        # print(my_eth.get_block(20))
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