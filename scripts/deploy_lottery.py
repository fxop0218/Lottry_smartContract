

from scripts.helpful_scripts import get_account
from scripts.helpful_scripts import get_account, get_contract
from brownie import Lottery

def main():
    deploy_lottery()

def deploy_lottery():
    accoutn = get_account(id="fxop02")
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address
    )