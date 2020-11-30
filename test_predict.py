import pytest

import predict
import datamanager


def test_line34():
    # some simple to hand calculate examples should suffice for now
    d = list(range(12))
    third_mean = (6 + 7 + 8)/3
    fourth_mean = (9 + 10 + 11)/3
    assert predict.line34(d) == (fourth_mean / third_mean)


@pytest.fixture
def data():
    assets = [ "eth", "dai" ]
    protocols = [ "compound", "aave", "dydx" ]
    pairsdf = datamanager.obtain(protocols, assets)
    return pairsdf