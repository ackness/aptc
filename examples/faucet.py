from aptc import new_client, Account

account = Account.generate()

print('account address:', account.address())
print('account private key:', account.private_key)

faucet_client = new_client(faucet=True)
txn_hash = faucet_client.deposit(account.address())
print(txn_hash)
