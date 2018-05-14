import pytest

from solc import compile_source

from ethpm.utils.bytecode_validation import (
    compare_bytecode,
    verify_contract_runtime_bytecode,
)


@pytest.mark.parametrize(
    "left,right,expected",
    (
        ("0x", "0x", True),
        ("", "0x", True),
        ("0x", "", True),
        ("", "", True),
        ("0x1234567890abcdef", "0x1234567890abcdef", True),
        ("1234567890abcdef", "0x1234567890abcdef", True),
        ("0x1234567890abcdef", "1234567890abcdef", True),
        ("0x1234567890abcdef", "0x", False),
        # with swarm hash.
        (
            "0x6060604052346000575b5b5b60358060186000396000f30060606040525b60005600a165627a7a72305820ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff0029",  # noqa: E501
            "0x6060604052346000575b5b5b60358060186000396000f30060606040525b60005600a165627a7a72305820eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee0029",  # noqa: E501
            True,
        ),
        # only swarm hash
        (
            "0xa165627a7a72305820ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff0029",  # noqa: E501
            "0xa165627a7a72305820eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee0029",  # noqa: E501
            True,
        ),
        # bad embedded swarm hash (too few bytes in hash)"
        (
            "0x6060604052346000575b5b5b60358060186000396000f30060606040525b60005600a165627a7a72305820ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff0029",  # noqa: E501
            "0x6060604052346000575b5b5b60358060186000396000f30060606040525b60005600a165627a7a72305820eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee0029",  # noqa: E501
            False,
        ),
        # bad embedded swarm hash (bad wrapping bytes)"
        (
            # should end with 29
            "0x6060604052346000575b5b5b60358060186000396000f30060606040525b60005600a165627a7a72305820ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff0028",  # noqa: E501
            # should end with 29
            "0x6060604052346000575b5b5b60358060186000396000f30060606040525b60005600a165627a7a72305820eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee0028",  # noqa: E501
            False,
        ),
    ),
)
def test_compare_bytecode(left, right, expected):
    actual = compare_bytecode(left, right)
    assert actual is expected


def test_runtime_bytecode_verification(valid_package_and_contract, w3):
    valid_package, contract_source_code = valid_package_and_contract
    compiled_sol = compile_source(contract_source_code)
    contract_interface = compiled_sol['<stdin>:SafeMathLib']
    SafeMathLib = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
    tx_hash = SafeMathLib.constructor().transact()
    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
    address = tx_receipt['contractAddress']
    expected = valid_package['contract_types']['SafeMathLib']['runtime_bytecode']['bytecode']
    # normalize runtime bytecode i.e. insert contract address after `0x73`
    norm_exp = expected.replace('0000000000000000000000000000000000000000', address[2:].lower(), 1)
    actual = verify_contract_runtime_bytecode(w3, norm_exp, address)
    assert actual is None
