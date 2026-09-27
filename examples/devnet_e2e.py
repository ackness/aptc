"""End-to-end example on devnet:

generate an account -> faucet mint -> sign -> submit -> wait -> check balance.

Run with: uv run python examples/devnet_e2e.py
"""

import time

from aptc import Account, new_client

# devnet node client + devnet faucet client
client = new_client(network="devnet")
faucet = new_client(faucet=True, network="devnet")

sender = Account.generate()
receiver = Account.generate()
print("sender:  ", sender.address())
print("receiver:", receiver.address())

# 1. mint some APT to the sender on devnet
mint_hash = faucet.deposit(sender.address())
print("mint txn:", mint_hash)
client.wait_for_transaction(mint_hash, timeout=30)
print("sender balance:", client.get_account_balance(sender.address()))

# 2. transfer 1000 octas to the receiver
amount = 1000
txn_dict = {
    "sender": sender.address().hex(),
    "sequence_number": str(client.get_account_sequence_number(sender.address())),
    "max_gas_amount": "100000",
    "gas_unit_price": "100",
    "expiration_timestamp_secs": str(int(time.time()) + 600),
    "payload": {
        "type": "entry_function_payload",
        "function": "0x1::aptos_account::transfer",
        "type_arguments": [],
        "arguments": [receiver.address().hex(), str(amount)],
    },
}

# encode -> sign -> submit -> wait
encoded = client.encode_submission(txn_dict)
signature = sender.sign(encoded)
txn_dict["signature"] = {
    "type": "ed25519_signature",
    "public_key": f"{sender.public_key()}",
    "signature": f"{signature}",
}
tx = client.submit_transaction(txn_dict)
print("submitted:", tx["hash"])

committed = client.wait_for_transaction(tx["hash"], timeout=30)
print("success:", committed["success"])
print("receiver balance:", client.get_account_balance(receiver.address()))
