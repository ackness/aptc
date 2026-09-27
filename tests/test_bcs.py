# Copyright (c) Aptos
# SPDX-License-Identifier: Apache-2.0

import pytest

from aptc import Deserializer, Serializer


def roundtrip(write, read, in_value):
    ser = Serializer()
    write(ser, in_value)
    der = Deserializer(ser.output())
    return read(der)


def test_bool_true():
    assert roundtrip(Serializer.bool, Deserializer.bool, True) is True


def test_bool_false():
    assert roundtrip(Serializer.bool, Deserializer.bool, False) is False


def test_bool_error():
    ser = Serializer()
    ser.u8(32)
    der = Deserializer(ser.output())
    with pytest.raises(Exception):
        der.bool()


def test_bytes():
    in_value = b"1234567890"
    assert roundtrip(Serializer.bytes, Deserializer.bytes, in_value) == in_value


def test_map():
    in_value = {"a": 12345, "b": 99234, "c": 23829}
    ser = Serializer()
    ser.map(in_value, Serializer.str, Serializer.u32)
    der = Deserializer(ser.output())
    assert der.map(Deserializer.str, Deserializer.u32) == in_value


def test_sequence():
    in_value = ["a", "abc", "def", "ghi"]
    ser = Serializer()
    ser.sequence(in_value, Serializer.str)
    der = Deserializer(ser.output())
    assert der.sequence(Deserializer.str) == in_value


def test_sequence_serializer():
    in_value = ["a", "abc", "def", "ghi"]
    ser = Serializer()
    seq_ser = Serializer.sequence_serializer(Serializer.str)
    seq_ser(ser, in_value)
    der = Deserializer(ser.output())
    assert der.sequence(Deserializer.str) == in_value


def test_str():
    in_value = "1234567890"
    assert roundtrip(Serializer.str, Deserializer.str, in_value) == in_value


def test_u8():
    assert roundtrip(Serializer.u8, Deserializer.u8, 15) == 15


def test_u16():
    assert roundtrip(Serializer.u16, Deserializer.u16, 11115) == 11115


def test_u32():
    assert roundtrip(Serializer.u32, Deserializer.u32, 1111111115) == 1111111115


def test_u64():
    in_value = 1111111111111111115
    assert roundtrip(Serializer.u64, Deserializer.u64, in_value) == in_value


def test_u128():
    in_value = 1111111111111111111111111111111111115
    assert roundtrip(Serializer.u128, Deserializer.u128, in_value) == in_value


def test_uleb128():
    in_value = 1111111115
    assert roundtrip(Serializer.uleb128, Deserializer.uleb128, in_value) == in_value
