from aptc import new_client

client = new_client()
some_address = "0xdc7ba0a76651c240f7ce55eec51209517a19d4c8d640460ab4789994c0256b15"
infos = client.get_account_resources(some_address)
infos2 = client.get_account_modules(some_address)
infos3 = client.get_account_resource(
    "0x8d763223180a2b92f97755a3ea581f1c68d342275ca6118badff663f57aca7a5",  # someones address
    "0xf9bf19f5077c196e5468510e140d1e3cbfa0681f67fe245566ceab2399a6388d::factory::MintedByUser"  # resource type
)
