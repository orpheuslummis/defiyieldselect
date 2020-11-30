"""
v0: protocol0 → eth → protocol1

v1: protocol0(asset0) → asset0 → asset1 → protocol1(asset1)
"""
import main
import account
import contracts_info
from web3 import Web3


class Protocol:
    """enter and exit"""
    def enter(self):
        print('entering')

    def exit(self):
        print('exiting')


class Aave(Protocol):
    """
    https://docs.aave.com/developers/developing-on-aave/the-protocol/safety-module-stkaave#integrating-staking

    approve() the amount for the Staked AAVE contract to stake
    stake()

    getTotalRewardsBalance()
    claimRewards()

    cooldown()
    # wait stakersCooldown()+COOLDOWN_SECONDS() until the cooldown finishes
    # we have until UNSTAKE_WINDOW() of time to redeem
    redeem()
    """
    pass


class Dydx(Protocol):
    pass


class Compound(Protocol):
    # before being able to supply, we need the account to enter the market 
    # different process for cETH than cERC20
    # NOTE that the account will also accumulate COMP tokens over time...
    
    def __init__(self, w3):
        self.w3 = w3
        address = Web3.toChecksumAddress(contracts_info.compound['Comptroller'])
        self.troll = w3.eth.contract(
            address=address, 
            abi=contracts_info.get_abi("compound2")
        )

    def enter(self):
        pass
        # const cTokens = [CErc20.at(0x3FDA...), CEther.at(0x3FDB...)];
        # const errors = await troll.methods.enterMarkets(cTokens).send({from: ...});
    
    def supply(self, amount):
        pass
        # cEthContract.methods.mint().send({
        #     from: myWalletAddress,
        #     gasLimit: web3.utils.toHex(150000),
        #     gasPrice: web3.utils.toHex(20000000000), // use ethgasstation.info (mainnet only)
        #     value: web3.utils.toHex(web3.utils.toWei('1', 'ether'))
        # });

    def withdraw(self, amount):
        pass
        # await cEthContract.methods.redeem(cTokenBalance * 1e8).send({
        #     from: myWalletAddress,
        #     gasLimit: web3.utils.toHex(500000),
        #     gasPrice: web3.utils.toHex(20000000000), // use ethgasstation.info (mainnet only)
        # });
