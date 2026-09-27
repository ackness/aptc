# Aptos Labs hosted fullnode REST API endpoints (Node API /v1).
# `api.{network}.aptoslabs.com` is the preferred hostname;
# `fullnode.{network}.aptoslabs.com` remains as an alias of the same service.
# Anonymous access works at a low rate limit; pass an API key
# (Authorization: Bearer <key>) via `HttpxProvider(url, api_key=...)` for more.

APTOS_NODE_URL_LIST = [
    "https://api.mainnet.aptoslabs.com/v1",
    "https://fullnode.mainnet.aptoslabs.com/v1",
]

TESTNET_APTOS_NODE_URL_LIST = [
    "https://api.testnet.aptoslabs.com/v1",
    "https://fullnode.testnet.aptoslabs.com/v1",
]

TESTNET_FAUCET_URL_LIST = [
    # Requires Google sign-in (JWT) since 2024; programmatic minting is disabled.
    "https://faucet.testnet.aptoslabs.com",
]

DEV_APTOS_NODE_URL_LIST = [
    "https://api.devnet.aptoslabs.com/v1",
    "https://fullnode.devnet.aptoslabs.com/v1",
]

DEV_FAUCET_URL_LIST = [
    "https://faucet.devnet.aptoslabs.com",
]

NODE_URLS = {
    "mainnet": APTOS_NODE_URL_LIST[0],
    "testnet": TESTNET_APTOS_NODE_URL_LIST[0],
    "devnet": DEV_APTOS_NODE_URL_LIST[0],
}

FAUCET_URLS = {
    "testnet": TESTNET_FAUCET_URL_LIST[0],
    "devnet": DEV_FAUCET_URL_LIST[0],
}
