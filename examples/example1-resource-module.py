from aptc import new_client

client = new_client()

# the framework account 0x1 always has resources and modules
some_address = "0x1"
infos = client.get_account_resources(some_address)
infos2 = client.get_account_modules(some_address)
infos3 = client.get_account_resource(
    some_address,
    "0x1::coin::CoinStore<0x1::aptos_coin::AptosCoin>",  # resource type
)
