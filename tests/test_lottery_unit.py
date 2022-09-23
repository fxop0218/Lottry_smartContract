from distutils.command.config import config
from operator import ne
from brownie import Lottery, accounts, network, config, exceptions
from web3 import Web3
from scripts.deploy_lottery import deploy_lottery
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENV, get_account, fund_with_link
import pytest

# Validate get entrance fee system
def test_get_entrance_fee():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV:
        pytest.skip()
    # Arrange
    lottery = deploy_lottery()
    # Act
    # Obtain 50 usd in eth for the test.0.039
    expected = Web3.toWei(0.0025, "ether")
    entrance_fee = lottery.getEntranceFee()
    # Assert
    assert expected == entrance_fee

# Validate enter system
def test_enter():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV: 
        pytest.skip()
    lottery = deploy_lottery()
    # Act and asset
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({"from" : get_account(), "value" : lottery.getEntranceFee()})

# Validate the user lottery player system
def test_can_start(): 
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV: 
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from" : account})
    lottery.enter({"from" : account, "value" : lottery.getEntranceFee()})
    assert lottery.players(0) == account

def test_can_end(): 
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV: 
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from" : account})
    lottery.enter({"from" : account, "value" : lottery.getEntranceFee()})
    fund_with_link(lottery)
    lottery.endLottery({"from" : account})
    assert lottery.lottery_state() == 2 # Position of the closed value
