OCTA = 1
APT = 100_000_000 * OCTA

APT_COIN_TYPE = "0x1::aptos_coin::AptosCoin"
COIN_STORE_TYPE_TAG = "0x1::coin::CoinStore<{type}>"
APT_COIN_STORE = COIN_STORE_TYPE_TAG.format(type=APT_COIN_TYPE)
