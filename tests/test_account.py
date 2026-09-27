# Copyright (c) Aptos
# SPDX-License-Identifier: Apache-2.0

from aptc import Account, AccountAddress


def test_load_and_store(tmp_path):
    path = tmp_path / "account.json"
    start = Account.generate()
    start.store(str(path))
    load = Account.load(str(path))

    assert start == load
    # Auth key and Account address should be the same at start
    assert start.address().hex() == start.auth_key()


def test_key():
    message = b"test message"
    account = Account.generate()
    signature = account.sign(message)
    assert account.public_key().verify(message, signature)


def test_load_key():
    account = Account.generate()
    loaded = Account.load_key(account.private_key.hex())
    assert loaded == account


def test_address_from_hex_pads_short_addresses():
    address = AccountAddress.from_hex("0x1")
    assert address.hex() == "0x" + "0" * 63 + "1"


def test_address_str_and_hex():
    account = Account.generate()
    assert str(account.address()) == account.address().hex()
    assert account.address().hex().startswith("0x")
    assert len(account.address().hex()) == 66
