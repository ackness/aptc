# Copyright (c) Aptos
# SPDX-License-Identifier: Apache-2.0

from aptc import Deserializer, Serializer
from aptc.sdk_impl.ed25519 import PrivateKey, PublicKey, Signature


def test_sign_and_verify():
    in_value = b"test_message"

    private_key = PrivateKey.random()
    public_key = private_key.public_key()

    signature = private_key.sign(in_value)
    assert public_key.verify(in_value, signature)


def test_verify_rejects_bad_message():
    private_key = PrivateKey.random()
    signature = private_key.sign(b"one message")
    assert not private_key.public_key().verify(b"another message", signature)


def test_private_key_serialization():
    private_key = PrivateKey.random()
    ser = Serializer()

    private_key.serialize(ser)
    ser_private_key = PrivateKey.deserialize(Deserializer(ser.output()))
    assert private_key == ser_private_key


def test_private_key_hex_roundtrip():
    private_key = PrivateKey.random()
    assert PrivateKey.from_hex(private_key.hex()) == private_key


def test_public_key_serialization():
    private_key = PrivateKey.random()
    public_key = private_key.public_key()

    ser = Serializer()
    public_key.serialize(ser)
    ser_public_key = PublicKey.deserialize(Deserializer(ser.output()))
    assert public_key == ser_public_key


def test_signature_serialization():
    private_key = PrivateKey.random()
    in_value = b"another_message"
    signature = private_key.sign(in_value)

    ser = Serializer()
    signature.serialize(ser)
    ser_signature = Signature.deserialize(Deserializer(ser.output()))
    assert signature == ser_signature
