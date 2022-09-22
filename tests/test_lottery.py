from distutils.command.config import config
from brownie import Lottery, accounts, network, config
from web3 import Web3

def test_get_entrance_fee():
    account = accounts[0]
    lottery = Lottery.deploy(config["networks"][network.show_active()]["eth_usd_price_feed"], {"from" : account})
    assert lottery.getEntraceFee() > Web3.toWei(0.020, "ether")
    assert lottery.getEntraceFee() < Web3.toWei(0.222, "ether")