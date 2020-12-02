import json
from datetime import datetime

import pytest
from web3 import Web3

import asset_movement


def test_compound_init(w3_connection):
    c = asset_movement.Compound(w3_connection)


def test_compound_enter(w3_connection):
    c = asset_movement.Compound(w3_connection)
    c.enter()


def test_compound_supply():
    pass


def test_compound_withdraw():
    pass


def test_aave_supply():
    pass


def test_aave_widthraw():
    pass


def test_read_compound_contracts_json():
    with open("abis/compound.json") as f:
        j = json.load(f)
        [print(k) for k in j]
        # print(j)
    # assert False


@pytest.fixture
def w3_connection():
    # assuming ganache-cli is running here
    return Web3(Web3.WebsocketProvider('ws://127.0.0.1:8545'))
