import json
import pytest


ABI_A = json.loads('[{"constant":false,"inputs":[],"name":"a","outputs":[],"type":"function"}]')
ABI_B = json.loads('[{"constant":false,"inputs":[{"name":"","type":"uint256"}],"name":"a","outputs":[],"type":"function"}]')
ABI_C = json.loads('[{"constant":false,"inputs":[],"name":"a","outputs":[],"type":"function"},{"constant":false,"inputs":[{"name":"","type":"bytes32"}],"name":"a","outputs":[],"type":"function"},{"constant":false,"inputs":[{"name":"","type":"uint256"}],"name":"a","outputs":[],"type":"function"}]')


@pytest.mark.parametrize(
    'abi,method,arguments,data,expected',
    (
        (ABI_A, 'a', [], None, '0x'),
        (ABI_A, 'a', [], '0x12345678', '0x12345678'),
        (ABI_B, 'a', [0], None, '0x0000000000000000000000000000000000000000000000000000000000000000'),
        (ABI_B, 'a', [1], None, '0x0000000000000000000000000000000000000000000000000000000000000001'),
        (ABI_C, 'a', [1], None, '0x0000000000000000000000000000000000000000000000000000000000000001'),
        (ABI_C, 'a', ['a'], None, '0x6100000000000000000000000000000000000000000000000000000000000000'),
    ),
)
def test_contract_abi_encoding(web3_tester, abi, method, arguments, data, expected):
    contract = web3_tester.eth.contract(abi)
    actual = contract.encodeABI(method, arguments, data=data)
    assert actual == expected
