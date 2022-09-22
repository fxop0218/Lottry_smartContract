from brownie import network, accounts, config
from web3 import Web3

DECIMALS = 8
STARTING_PRICE = 200000000000
FROKED_LOCAL_ENVIROMENTS = ["mainnet-fork","mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENV = ["decelopment", "ganache-local"]

def get_account(index=None, id=None):
    # accoutns[0]
    # accounts.add("env")
    # accounts.load("id")
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if(network.show_active() in LOCAL_BLOCKCHAIN_ENV):
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])