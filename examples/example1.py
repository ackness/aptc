from loguru import logger

from aptc import new_client

# init logger
logger.add("example1.log")

# mainnet client (use network="devnet"/"testnet" for the other networks)
client = new_client()

ledger = client.get_ledger_info()
logger.info(ledger)
logger.info(client.check_health())
logger.info(client.get_node_info())
logger.info(client.estimate_gas_price())

example_address = "0x1"  # the aptos framework account always exists
logger.info(client.get_account(example_address))
logger.info(client.get_account_balance(example_address))
logger.info(client.get_account_module(example_address, "coin"))

logger.info(client.get_account_transactions(example_address, limit=5))
logger.info(client.get_account_transaction_summaries(example_address))

# a read-only on-chain "view" call
logger.info(
    client.view_function(
        "0x1::coin::balance",
        type_arguments=["0x1::aptos_coin::AptosCoin"],
        arguments=[example_address],
    )
)

# recent committed transaction (old versions are pruned on public fullnodes)
logger.info(client.get_transaction_by_version(int(ledger["ledger_version"]) - 100))
