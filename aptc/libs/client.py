import time
from typing import Dict

from httpx import Response

from ._types import Address, TXHash, IntNumber
from .apis import APTTransactionsAPI, APTAccountAPI, APTGeneralAPI, APTBlockAPI, APTEventAPI, APTTablesAPI
from .errors import ParamsError, RPCRequestError
from .providers import BaseProvider


class BaseClient:
    def __init__(self, provider):
        self.provider = provider


class APTClient(BaseClient):
    BCS_SUBMIT_HEADERS = {'Content-Type': 'application/x.aptos.signed_transaction+bcs'}

    def __init__(self, provider: BaseProvider):
        super(APTClient, self).__init__(provider)
        self.provider = provider
        self.base_url = self.provider.base_url

    # account
    def get_account(self, address: Address) -> dict:
        return self.provider.get(APTAccountAPI.GET_ACCOUNT.format(address=address))

    account = get_account

    def get_account_resource(self, address: Address, resource_type: str) -> dict:
        return self.provider.get(
            APTAccountAPI.GET_ACCOUNT_RESOURCE.format(address=address, resource_type=resource_type))

    account_resource = get_account_resource

    def get_account_resources(self, address: Address) -> dict:
        return self.provider.get(APTAccountAPI.GET_ACCOUNT_RESOURCES.format(address=address))

    account_resources = get_account_resources

    def get_account_modules(self, address: Address) -> dict:
        return self.provider.get(APTAccountAPI.GET_ACCOUNT_MODULES.format(address=address))

    account_modules = get_account_modules

    def get_account_module(self, address: Address, module_name: str) -> dict:
        return self.provider.get(APTAccountAPI.GET_ACCOUNT_MODULE.format(address=address, module_name=module_name))

    account_module = get_account_module

    # useful account related method
    def get_account_balance(self, address: Address) -> int:
        # return self.get_account_resource(address, APT_COIN_STORE)['data']['coin']['value']
        return int(
            self.provider.get(APTAccountAPI.GET_ACCOUNT_BALANCE.format(address=address))['data']['coin']['value'])

    account_balance = get_account_balance

    def get_account_sequence_number(self, address: Address) -> int:
        return int(self.get_account(address)['sequence_number'])

    account_sequence_number = get_account_sequence_number
    sequence_number = get_account_sequence_number

    def get_account_nonce(self, address: Address) -> int:
        return int(self.get_account_sequence_number(address))

    account_nonce = get_account_nonce

    # block
    def get_block_by_height(self, block_height: IntNumber) -> dict:
        return self.provider.get(APTBlockAPI.GET_BLOCK_BY_HEIGHT.format(block_height=str(block_height)))

    block_by_height = get_block_by_height

    def get_block_by_version(self, version: IntNumber) -> dict:
        return self.provider.get(APTBlockAPI.GET_BLOCK_BY_VERSION.format(version=str(version)))

    block_by_version = get_block_by_version

    # event
    def get_event_by_creation_number(self, address: Address, creation_number: int) -> dict:
        return self.provider.get(
            APTEventAPI.GET_EVENT_BY_CREATION_NUMBER.format(address=address, creation_number=str(creation_number)))

    event_by_creation_number = get_event_by_creation_number

    def get_event_by_event_handle(self, address: Address, event_handle: str) -> dict:
        return self.provider.get(
            APTEventAPI.GET_EVENT_BY_EVENT_HANDLE.format(address=address, event_handle=event_handle))

    event_by_event_handle = get_event_by_event_handle

    # general
    def show_openapi_explorer(self) -> dict:
        url = self.provider.patch_url([self.provider.base_url, APTGeneralAPI.SHOW_OPENAPI_EXPLORER])
        return self.provider.client.get(url)

    def check_node_health(self) -> dict:
        return self.provider.get(APTGeneralAPI.CHECK_NODE_HEALTH)

    check_health = check_node_health

    def get_ledger_info(self):
        # some node may not support this api
        return self.provider.get(APTGeneralAPI.GET_LEDGER_INFO)

    ledger_info = get_ledger_info

    # tables
    def get_table_item(self, table_handle: str) -> dict:
        return self.provider.post(APTTablesAPI.GET_TABLE_ITEM.format(table_handle=table_handle))

    table_item = get_table_item

    # transactions
    def get_transactions(self) -> dict:
        return self.provider.get(APTTransactionsAPI.GET_TRANSACTIONS)

    transactions = get_transactions

    def get_transaction_by_hash(self, txn_hash: TXHash) -> dict:
        return self.provider.get(APTTransactionsAPI.GET_TRANSACTION_BY_HASH.format(txn_hash=txn_hash))

    get_txn_by_hash = get_transaction_by_hash

    def get_transaction_by_version(self, txn_version: IntNumber) -> dict:
        return self.provider.get(APTTransactionsAPI.GET_TRANSACTION_BY_VERSION.format(txn_version=str(txn_version)))

    transaction_by_version = get_transaction_by_version

    def get_account_transactions(self, address) -> dict:
        return self.provider.get(APTTransactionsAPI.GET_ACCOUNT_TRANSACTIONS.format(address=address))

    account_transactions = get_account_transactions

    def submit_transaction(self, txn_dict: Dict):
        return self.provider.post(
            APTTransactionsAPI.SUBMIT_TRANSACTION, params_dict=txn_dict,
            # headers=self.provider.DEFAULT_HEADERS
        )

    submit = submit_transaction

    def submit_batch_transactions(self, batch_txn_dict: Dict):
        return self.provider.post(
            APTTransactionsAPI.SUBMIT_BATCH_TRANSACTIONS, params_dict=batch_txn_dict,
            # headers=self.provider.DEFAULT_HEADERS
        )

    submit_batch = submit_batch_transactions

    def simulate_transaction(
            self, txn_dict, estimate_gas_unit_price: str = "false",
            estimate_max_gas_amount: str = "false",
            estimate_prioritized_gas_unit_price: str = "false"
    ):
        j = self.provider.post(
            f'{APTTransactionsAPI.SIMULATE_TRANSACTION}'
            f'?estimate_gas_unit_price={estimate_gas_unit_price}'
            f'&estimate_max_gas_amount={estimate_max_gas_amount}'
            f'&estimate_prioritized_gas_unit_price={estimate_prioritized_gas_unit_price}',
            txn_dict,
        )
        return self._handle_simulate_error(j)

    simulate = simulate_transaction

    def encode_submission(self, txn_dict: Dict):
        j = self.provider.post(APTTransactionsAPI.ENCODE_SUBMISSION, params_dict=txn_dict)
        if "message" in j:
            raise RPCRequestError(j["message"])
        else:
            return bytes.fromhex(j[2:])

    encode = encode_submission

    @staticmethod
    def _handle_simulate_error(j: Response):
        if isinstance(j, list):
            j = j[0]
        else:
            raise ParamsError(f"Check Txn dict Params. RPC Response: {j}")

        if j['success']:
            return j
        else:
            raise RPCRequestError(f"RPC Error: {j['vm_status']}")

    def transaction_pending(self, txn_hash: str) -> bool:
        response = self.provider.client.get(f"{self.base_url}/transactions/by_hash/{txn_hash}")
        # print(response)
        if response.status_code == 404:
            return True
        if response.status_code >= 400:
            raise RPCRequestError(response.text, response.status_code)
        return response.json()["type"] == "pending_transaction"

    def wait_for_transaction(self, txn_hash, timeout=10, iteration=1):
        """Waits up to 20 seconds for a transaction to move past pending state."""

        count = 0
        while self.transaction_pending(txn_hash):
            assert count < timeout, f"transaction {txn_hash} timed out"
            time.sleep(iteration)
            count += iteration
        response = self.provider.get(f"{self.base_url}/transactions/by_hash/{txn_hash}")
        assert (
                "success" in response.json() and response.json()["success"]
        ), f"{response.text} - {txn_hash}"


class APTDevClient(APTClient):
    def __init__(self, provider: BaseProvider):
        super(APTDevClient, self).__init__(provider)
        self.provider = provider

    def deposit(self, address: Address, amount: int = 10_000_000) -> str:
        response = self.provider.client.post(f"{self.base_url}/mint?amount={amount}&address={address}")
        if response.status_code >= 400:
            raise RPCRequestError(response.text, response.status_code)
        # for testnet it not return proper response, but still success
        return response.json()[0]
