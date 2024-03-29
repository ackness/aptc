import os
import time

from loguru import logger

from aptc import Account, APT, new_client
from aptc.libs import build_transfer_payload

# init logger
logger.add("example2.log")

client = new_client()

# submit transaction
# load your private key
account = Account.load_key(os.environ['private_key'])
account_address = account.address()
receiver_address = "0x8d763223180a2b92f97755a3ea581f1c68d342275ca6118badff663f57aca7a5"

payload_1 = build_transfer_payload(receiver_address, int(0.1 * APT))
payload_2 = build_transfer_payload(receiver_address, int(0.2 * APT))

txn_dict = {
    "sender": f"{account_address}",
    "sequence_number": str(client.get_account_sequence_number(account_address)),
    "max_gas_amount": str(100_000),
    "gas_unit_price": str(100),
    "expiration_timestamp_secs": str(int(time.time()) + 100),
    "payload": [payload_1, payload_2],
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
