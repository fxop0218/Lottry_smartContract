
import time
from dis import show_code
from typing import NewType
from scripts.helpful_scripts import get_account, get_contract, fund_with_link
from brownie import Lottery, network, config

def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()

def deploy_lottery():
    account = get_account()
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print("Deployed lottery!")
    return lottery

def start_lottery():
    accoutn = get_account()
    lottery = Lottery[-1] # get recent deployment
    starting_tx = lottery.startLottery({"from" : accoutn})
    starting_tx.wait(1)
    print("Lottey started")

def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + 10**8
    transaction = lottery.enter({"from" : account, "value" : value})
    transaction.wait(1)
    print("You entered the lottery")

def end_lottery(): 
    account = get_account()
    lottery = Lottery[-1]
    print("El pepe")
    # fund the contract
    # then end the lottery
    transaction = fund_with_link(lottery.address)
    transaction.wait(1)
    ending_transaction = lottery.endLottery({"from": account})
    ending_transaction.wait(1)
    time.sleep(180)
    print(f"{lottery.recentWinner()} is the new winner!")

