import time

from loguru import logger

from aptc import APTClient, HttpxProvider, APTOS_NODE_URL_LIST, Account, APT

# init logger
logger.add("example2.log")

APT_NODE_URL = APTOS_NODE_URL_LIST[0]
client = APTClient(HttpxProvider(APT_NODE_URL))
logger.info(f"NODE: {APT_NODE_URL}")

# submit transaction
# load your private key
account = Account.load_key("")
account_address = account.address()

# build a transaction payload
payload = {
    'function': '0x1::aptos_account::transfer',
    'type_arguments': [],
    'arguments': [
        "0x8d763223180a2b92f97755a3ea581f1c68d342275ca6118badff663f57aca7a5",  # receiver
        str(1 * APT)  # amount
    ],
    'type': 'entry_function_payload'
}
txn_dict = {
    "sender": f"{account_address}",
    "sequence_number": str(client.get_account_sequence_number(account_address)),
    "max_gas_amount": str(100_000),
    "gas_unit_price": str(100),
    "expiration_timestamp_secs": str(int(time.time()) + 100),
    "payload": payload,
}
# encode this transaction
encoded = client.encode(txn_dict)
# sign this transaction
signature = account.sign(encoded)

txn_dict["signature"] = {
    "type": "ed25519_signature",
    "public_key": f"{account.public_key()}",
    "signature": f"{signature}",
}

# submit transaction
tx = client.submit_transaction(txn_dict)
