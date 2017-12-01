import pytest

from web3 import Web3
from web3.providers.eth_tester import EthereumTesterProvider
from eth_tester import (
    EthereumTester,
    MockBackend,
)


@pytest.fixture()
def w3():
    eth_tester = EthereumTester(MockBackend())
    w3 = Web3(EthereumTesterProvider(eth_tester))
    return w3
