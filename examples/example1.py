from loguru import logger

from aptc import APTClient, HttpxProvider, APTOS_NODE_URL_LIST

# init logger
logger.add("example1.log")

APT_NODE_URL = APTOS_NODE_URL_LIST[0]
client = APTClient(HttpxProvider(APT_NODE_URL))
logger.info(f"NODE: {APT_NODE_URL}")

logger.info(client.get_ledger_info())
logger.info(client.check_health())
# logger.info(client.show_openapi_explorer())

example_address = '0xc739507214d0e1bf9795485299d709e00024e92f7c0d055a4c2c39717882bdfd'
logger.info(client.get_account(example_address))
logger.info(client.get_account_balance(example_address))
logger.info(client.get_account_resources(example_address))
logger.info(client.get_account_transactions(example_address))

logger.info(client.get_txn_by_hash('0xf82981720faf0c78c06e17764af42741208c1600df497a9c8066d1e91b9635e8'))
logger.info(client.get_account_sequence_number(example_address))

logger.info(client.get_transaction_by_version(99999))
