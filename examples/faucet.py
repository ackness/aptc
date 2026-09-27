from aptc import Account, new_client

account = Account.generate()

print("account address:", account.address())
print("account private key:", account.private_key)

# devnet faucet — the testnet faucet requires Google sign-in (JWT)
# and no longer supports programmatic minting.
faucet_client = new_client(faucet=True, network="devnet")
txn_hash = faucet_client.deposit(account.address())
print(txn_hash)
