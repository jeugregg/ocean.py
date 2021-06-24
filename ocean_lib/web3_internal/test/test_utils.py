#
# Copyright 2021 Ocean Protocol Foundation
# SPDX-License-Identifier: Apache-2.0
#
import os

import pytest

from ocean_lib.web3_internal.transactions import (
    cancel_or_replace_transaction,
    send_ether,
)
from ocean_lib.web3_internal.utils import (
    generate_multi_value_hash,
    prepare_prefixed_hash,
)


def test_generate_multi_value_hash(alice_address, alice_private_key):
    with pytest.raises(AssertionError):
        generate_multi_value_hash(["more", "types", "than"], ["values"])

    expected = "0x6d59f15c5814d9fddd2e69d1f6f61edd0718e337c41ec74011900c0d736a9fec"
    assert alice_private_key == os.getenv("TEST_PRIVATE_KEY1")
    assert alice_address == "0x66aB6D9362d4F35596279692F0251Db635165871"
    tested = generate_multi_value_hash(["address"], [alice_address]).hex()
    assert tested == expected, "The tested address is not the expected one."


def test_prepare_fixed_hash():
    expected = "0x5662cc8481d004c9aff44f15f3ed133dd54f9cfba0dbf850f69b1cbfc50145bf"
    assert (
        prepare_prefixed_hash("0x0").hex() == expected
    ), "The address is not the expected one."


def test_chain_id_send_ether(alice_wallet, bob_address, web3_instance):
    receipt = send_ether(alice_wallet, bob_address, 1)
    if not receipt:
        raise AssertionError("Send ether was unsuccessful.")
    tx = web3_instance.eth.get_transaction(receipt["transactionHash"])
    # Geth private chains (default), the chainId will be 1337
    expected_chain_ids = [1336, 1337]
    # Formula: v = CHAIN_ID * 2 + 35 or v = CHAIN_ID * 2 + 36
    chain_ids = [(tx["v"] - 35) / 2, (tx["v"] - 36) / 2]
    result = any(map(lambda chain_id: chain_id in expected_chain_ids, chain_ids))
    assert result


def test_chain_id_cancel_or_replace_transaction(
    alice_wallet, bob_address, web3_instance
):
    receipt_cancelled = cancel_or_replace_transaction(alice_wallet, None)
    if not receipt_cancelled:
        raise AssertionError("Cancel or replace transaction failed.")
    tx_cancelled = web3_instance.eth.get_transaction(
        receipt_cancelled["transactionHash"]
    )
    expected_chain_ids = [1336, 1337]
    chain_ids = [(tx_cancelled["v"] - 35) / 2, (tx_cancelled["v"] - 36) / 2]
    result_cancelled = any(
        map(lambda chain_id: chain_id in expected_chain_ids, chain_ids)
    )
    assert result_cancelled


def test_send_ether(alice_wallet, bob_address):
    assert send_ether(alice_wallet, bob_address, 1), "Send ether was unsuccessful."


def test_cancel_or_replace_transaction(alice_wallet):
    assert cancel_or_replace_transaction(
        alice_wallet, None
    ), "Cancel or replace transaction failed."
