from typing import Dict

from httpx import Response

from ._types import Address, TXHash, IntNumber
from .apis import APTTransactionsAPI, APTAccountAPI, APTGeneralAPI, APTBlockAPI, APTEventAPI, APTTablesAPI
from .errors import ParamsError, RPCRequestError
from .providers import BaseProvider


class APTClient:
    def __init__(self, provider: BaseProvider):
        self.provider = provider

    # account
    def get_account(self, address: Address):
        return self.provider.get(APTAccountAPI.GET_ACCOUNT.format(address=address))

    def get_account_resource(self, address: Address, resource_type: str):
        return self.provider.get(
            APTAccountAPI.GET_ACCOUNT_RESOURCE.format(address=address, resource_type=resource_type))

    def get_account_resources(self, address: Address):
        return self.provider.get(APTAccountAPI.GET_ACCOUNT_RESOURCES.format(address=address))

    def get_account_modules(self, address: Address):
        return self.provider.get(APTAccountAPI.GET_ACCOUNT_MODULES.format(address=address))

    def get_account_module(self, address: Address, module_name: str):
        return self.provider.get(APTAccountAPI.GET_ACCOUNT_MODULE.format(address=address, module_name=module_name))

    # useful account related method
    def get_account_balance(self, address: Address):
        # return self.get_account_resource(address, APT_COIN_STORE)['data']['coin']['value']
        return self.provider.get(APTAccountAPI.GET_ACCOUNT_BALANCE.format(address=address))['data']['coin']['value']

    def get_account_sequence_number(self, address: Address):
        return self.get_account(address)['sequence_number']

    def get_account_nonce(self, address: Address):
        return self.get_account_sequence_number(address)

    # block
    def get_block_by_height(self, block_height: IntNumber):
        return self.provider.get(APTBlockAPI.GET_BLOCK_BY_HEIGHT.format(block_height=str(block_height)))

    def get_block_by_version(self, version: IntNumber):
        return self.provider.get(APTBlockAPI.GET_BLOCK_BY_VERSION.format(version=str(version)))

    # event
    def get_event_by_creation_number(self, address: Address, creation_number: int):
        return self.provider.get(
            APTEventAPI.GET_EVENT_BY_CREATION_NUMBER.format(address=address, creation_number=str(creation_number)))

    def get_event_by_event_handle(self, address: Address, event_handle: str):
        return self.provider.get(
            APTEventAPI.GET_EVENT_BY_EVENT_HANDLE.format(address=address, event_handle=event_handle))

    # general
    def show_openapi_explorer(self):
        url = self.provider.patch_url([self.provider.base_url, APTGeneralAPI.SHOW_OPENAPI_EXPLORER])
        return self.provider.client.get(url)

    def check_node_health(self):
        return self.provider.get(APTGeneralAPI.CHECK_NODE_HEALTH)

    check_health = check_node_health

    def get_ledger_info(self):
        return self.provider.get(APTGeneralAPI.GET_LEDGER_INFO)

    # tables
    def get_table_item(self, table_handle: str):
        return self.provider.post(APTTablesAPI.GET_TABLE_ITEM.format(table_handle=table_handle))

    # transactions
    def get_transactions(self):
        return self.provider.get(APTTransactionsAPI.GET_TRANSACTIONS)

    def get_transaction_by_hash(self, txn_hash: TXHash):
        return self.provider.get(APTTransactionsAPI.GET_TRANSACTION_BY_HASH.format(txn_hash=txn_hash))

    get_txn_by_hash = get_transaction_by_hash

    def get_transaction_by_version(self, txn_version: IntNumber):
        return self.provider.get(APTTransactionsAPI.GET_TRANSACTION_BY_VERSION.format(txn_version=str(txn_version)))

    def get_account_transactions(self, address):
        return self.provider.get(APTTransactionsAPI.GET_ACCOUNT_TRANSACTIONS.format(address=address))

    def submit_transaction(self, txn_dict: Dict):
        return self.provider.post(APTTransactionsAPI.SUBMIT_TRANSACTION, params_dict=txn_dict)

    submit = submit_transaction

    def submit_batch_transactions(self, batch_txn_dict: Dict):
        return self.provider.post(APTTransactionsAPI.SUBMIT_BATCH_TRANSACTIONS, params_dict=batch_txn_dict)

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
            txn_dict
        )
        return self._handle_simulate_error(j)

    simulate = simulate_transaction

    def encode_submission(self, txn_dict: Dict):
        j = self.provider.post(APTTransactionsAPI.ENCODE_SUBMISSION, params_dict=txn_dict)
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
