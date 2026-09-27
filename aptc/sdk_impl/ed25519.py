# Copyright (c) Aptos
# SPDX-License-Identifier: Apache-2.0

from nacl.signing import SigningKey, VerifyKey

from .bcs import Deserializer, Serializer


class PrivateKey:
    LENGTH: int = 32

    key: SigningKey

    def __init__(self, key: SigningKey):
        self.key = key

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PrivateKey):
            return NotImplemented
        return self.key == other.key

    def __str__(self):
        return self.hex()

    @classmethod
    def from_hex(cls, value: str) -> PrivateKey:
        value = value.removeprefix("0x")
        return PrivateKey(SigningKey(bytes.fromhex(value)))

    def hex(self) -> str:
        return f"0x{self.key.encode().hex()}"

    def public_key(self) -> PublicKey:
        return PublicKey(self.key.verify_key)

    @classmethod
    def random(cls) -> PrivateKey:
        return PrivateKey(SigningKey.generate())

    def sign(self, data: bytes) -> Signature:
        return Signature(self.key.sign(data).signature)

    @classmethod
    def deserialize(cls, deserializer: Deserializer) -> PrivateKey:
        key = deserializer.bytes()
        if len(key) != PrivateKey.LENGTH:
            raise Exception("Length mismatch")

        return PrivateKey(SigningKey(key))

    def serialize(self, serializer: Serializer):
        serializer.bytes(self.key.encode())


class PublicKey:
    LENGTH: int = 32

    key: VerifyKey

    def __init__(self, key: VerifyKey):
        self.key = key

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PublicKey):
            return NotImplemented
        return self.key == other.key

    def __str__(self) -> str:
        return f"0x{self.key.encode().hex()}"

    def verify(self, data: bytes, signature: Signature) -> bool:
        try:
            self.key.verify(data, signature.data())
        except Exception:
            return False
        return True

    @classmethod
    def deserialize(cls, deserializer: Deserializer) -> PublicKey:
        key = deserializer.bytes()
        if len(key) != PublicKey.LENGTH:
            raise Exception("Length mismatch")

        return PublicKey(VerifyKey(key))

    def serialize(self, serializer: Serializer):
        serializer.bytes(self.key.encode())


class Signature:
    LENGTH: int = 64

    signature: bytes

    def __init__(self, signature: bytes):
        self.signature = signature

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Signature):
            return NotImplemented
        return self.signature == other.signature

    def __str__(self) -> str:
        return f"0x{self.signature.hex()}"

    def data(self) -> bytes:
        return self.signature

    @classmethod
    def deserialize(cls, deserializer: Deserializer) -> Signature:
        signature = deserializer.bytes()
        if len(signature) != Signature.LENGTH:
            raise Exception("Length mismatch")

        return Signature(signature)

    def serialize(self, serializer: Serializer):
        serializer.bytes(self.signature)
