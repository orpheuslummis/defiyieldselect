"""
v0: protocol0 → eth → protocol1

v1: protocol0(asset0) → asset0 → asset1 → protocol1(asset1)
"""

import web3

import main
import account
import contracts_info


class Protocol:
    """enter and exit"""
    def enter(self):
        print('entering')

    def exit(self):
        print('exiting')


class Aave(Protocol):
    pass


class Dydx(Protocol):
    pass


class Compound(Protocol):
    # before being able to supply, we need the account to enter the market 
    # different process for cETH than cERC20
    # NOTE that the account will also accumulate COMP tokens over time...

    def __init__(self):
        self.troll = w3.eth.contract(address=contracts_info.compound.Comptroller, abi=contracts_info.get_abi("compound_comptroller"))

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



if __name__ == "__main__":
    for p in main.protocols:
        print(f"eth → {p}\n{p} → eth")