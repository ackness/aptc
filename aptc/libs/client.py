import time

from httpx import Response

from ._types import Address, IntNumber, TXHash
from .apis import (
    APTAccountAPI,
    APTBlockAPI,
    APTEventAPI,
    APTGeneralAPI,
    APTTablesAPI,
    APTTransactionsAPI,
    APTViewAPI,
)
from .const import APT_COIN_TYPE
from .errors import ParamsError, RPCRequestError
from .providers import BaseProvider


class BaseClient:
    def __init__(self, provider):
        self.provider = provider


class APTClient(BaseClient):
    BCS_SUBMIT_HEADERS = {"Content-Type": "application/x.aptos.signed_transaction+bcs"}

    def __init__(self, provider: BaseProvider):
        super().__init__(provider)
        self.provider = provider
        self.base_url = self.provider.base_url

    # account
    def get_account(self, address: Address) -> dict:
        return self.provider.get(APTAccountAPI.GET_ACCOUNT.format(address=address))

    account = get_account

    def get_account_resource(self, address: Address, resource_type: str) -> dict:
        return self.provider.get(
            APTAccountAPI.GET_ACCOUNT_RESOURCE.format(
                address=address, resource_type=resource_type
            )
        )

    account_resource = get_account_resource

    def get_account_resources(self, address: Address) -> dict:
        return self.provider.get(
            APTAccountAPI.GET_ACCOUNT_RESOURCES.format(address=address)
        )

    account_resources = get_account_resources

    def get_account_modules(self, address: Address) -> dict:
        return self.provider.get(
            APTAccountAPI.GET_ACCOUNT_MODULES.format(address=address)
        )

    account_modules = get_account_modules

    def get_account_module(self, address: Address, module_name: str) -> dict:
        return self.provider.get(
            APTAccountAPI.GET_ACCOUNT_MODULE.format(
                address=address, module_name=module_name
            )
        )

    account_module = get_account_module

    # useful account related method
    def get_account_balance(
        self, address: Address, asset_type: str = APT_COIN_TYPE
    ) -> int:
        """Balance of a coin or the primary fungible-asset store for `asset_type`.

        Uses the `/accounts/{address}/balance/{asset_type}` endpoint so it keeps
        working for accounts without a legacy `CoinStore` resource.
        """
        return int(
            self.provider.get(
                APTAccountAPI.GET_ACCOUNT_BALANCE_BY_TYPE.format(
                    address=address, asset_type=asset_type
                )
            )
        )

    account_balance = get_account_balance

    def get_account_sequence_number(self, address: Address) -> int:
        return int(self.get_account(address)["sequence_number"])

    account_sequence_number = get_account_sequence_number
    sequence_number = get_account_sequence_number

    def get_account_nonce(self, address: Address) -> int:
        return int(self.get_account_sequence_number(address))

    account_nonce = get_account_nonce

    # block
    def get_block_by_height(self, block_height: IntNumber) -> dict:
        return self.provider.get(
            APTBlockAPI.GET_BLOCK_BY_HEIGHT.format(block_height=str(block_height))
        )

    block_by_height = get_block_by_height

    def get_block_by_version(self, version: IntNumber) -> dict:
        return self.provider.get(
            APTBlockAPI.GET_BLOCK_BY_VERSION.format(version=str(version))
        )

    block_by_version = get_block_by_version

    # event
    def get_event_by_creation_number(
        self, address: Address, creation_number: int
    ) -> dict:
        return self.provider.get(
            APTEventAPI.GET_EVENT_BY_CREATION_NUMBER.format(
                address=address, creation_number=str(creation_number)
            )
        )

    event_by_creation_number = get_event_by_creation_number

    def get_event_by_event_handle(
        self, address: Address, event_handle: str, field_name: str
    ) -> dict:
        return self.provider.get(
            APTEventAPI.GET_EVENT_BY_EVENT_HANDLE.format(
                address=address, event_handle=event_handle, field_name=field_name
            )
        )

    event_by_event_handle = get_event_by_event_handle

    # general
    def show_openapi_explorer(self) -> Response:
        url = self.provider.patch_url(
            [self.provider.base_url, APTGeneralAPI.SHOW_OPENAPI_EXPLORER]
        )
        return self.provider.client.get(url)

    def check_node_health(self) -> dict:
        return self.provider.get(APTGeneralAPI.CHECK_NODE_HEALTH)

    check_health = check_node_health

    def get_node_info(self) -> dict:
        return self.provider.get(APTGeneralAPI.GET_NODE_INFO)

    node_info = get_node_info

    def get_ledger_info(self):
        # some node may not support this api
        return self.provider.get(APTGeneralAPI.GET_LEDGER_INFO)

    ledger_info = get_ledger_info

    # tables
    def get_table_item(
        self,
        table_handle: str,
        key,
        key_type: str,
        value_type: str,
        ledger_version: IntNumber | None = None,
    ) -> dict:
        api = APTTablesAPI.GET_TABLE_ITEM.format(table_handle=table_handle)
        if ledger_version is not None:
            api = f"{api}?ledger_version={ledger_version}"
        return self.provider.post(
            api,
            params_dict={
                "key": key,
                "key_type": key_type,
                "value_type": value_type,
            },
        )

    table_item = get_table_item

    def get_table_item_raw(
        self, table_handle: str, key: str, ledger_version: IntNumber | None = None
    ) -> dict:
        """Raw (BCS-encoded) table item; `key` is a hex-encoded BCS key."""
        api = APTTablesAPI.GET_TABLE_ITEM_RAW.format(table_handle=table_handle)
        if ledger_version is not None:
            api = f"{api}?ledger_version={ledger_version}"
        return self.provider.post(api, params_dict={"key": key})

    table_item_raw = get_table_item_raw

    # view functions
    def view_function(
        self,
        function: str,
        type_arguments: list[str] | None = None,
        arguments: list | None = None,
        ledger_version: IntNumber | None = None,
    ) -> list:
        api = APTViewAPI.VIEW_FUNCTION
        if ledger_version is not None:
            api = f"{api}?ledger_version={ledger_version}"
        return self.provider.post(
            api,
            params_dict={
                "function": function,
                "type_arguments": type_arguments or [],
                "arguments": arguments or [],
            },
        )

    view = view_function

    # transactions
    def get_transactions(
        self, start: IntNumber | None = None, limit: int | None = None
    ) -> dict:
        params = {}
        if start is not None:
            params["start"] = str(start)
        if limit is not None:
            params["limit"] = limit
        return self.provider.get(
            APTTransactionsAPI.GET_TRANSACTIONS, params_dict=params or None
        )

    transactions = get_transactions

    def get_transaction_by_hash(self, txn_hash: TXHash) -> dict:
        return self.provider.get(
            APTTransactionsAPI.GET_TRANSACTION_BY_HASH.format(txn_hash=txn_hash)
        )

    get_txn_by_hash = get_transaction_by_hash

    def wait_transaction_by_hash(self, txn_hash: TXHash) -> dict:
        """Long-poll variant of `get_transaction_by_hash` (Node API v1.1+)."""
        return self.provider.get(
            APTTransactionsAPI.WAIT_TRANSACTION_BY_HASH.format(txn_hash=txn_hash)
        )

    wait_txn_by_hash = wait_transaction_by_hash

    def get_transaction_by_version(self, txn_version: IntNumber) -> dict:
        return self.provider.get(
            APTTransactionsAPI.GET_TRANSACTION_BY_VERSION.format(
                txn_version=str(txn_version)
            )
        )

    transaction_by_version = get_transaction_by_version

    def get_account_transactions(
        self, address, start: IntNumber | None = None, limit: int | None = None
    ) -> dict:
        params = {}
        if start is not None:
            params["start"] = str(start)
        if limit is not None:
            params["limit"] = limit
        return self.provider.get(
            APTTransactionsAPI.GET_ACCOUNT_TRANSACTIONS.format(address=address),
            params_dict=params or None,
        )

    account_transactions = get_account_transactions

    def get_account_transaction_summaries(
        self,
        address: Address,
        start_version: IntNumber | None = None,
        end_version: IntNumber | None = None,
    ) -> dict:
        params = {}
        if start_version is not None:
            params["start_version"] = str(start_version)
        if end_version is not None:
            params["end_version"] = str(end_version)
        return self.provider.get(
            APTTransactionsAPI.GET_ACCOUNT_TRANSACTION_SUMMARIES.format(
                address=address
            ),
            params_dict=params or None,
        )

    account_transaction_summaries = get_account_transaction_summaries

    def get_transactions_auxiliary_info(
        self, start_version: IntNumber, limit: int | None = None
    ) -> dict:
        params = {"start_version": str(start_version)}
        if limit is not None:
            params["limit"] = limit
        return self.provider.get(
            APTTransactionsAPI.GET_TRANSACTIONS_AUXILIARY_INFO, params_dict=params
        )

    transactions_auxiliary_info = get_transactions_auxiliary_info

    def estimate_gas_price(self) -> dict:
        return self.provider.get(APTTransactionsAPI.ESTIMATE_GAS_PRICE)

    gas_price = estimate_gas_price

    def submit_transaction(self, txn_dict: dict):
        return self.provider.post(
            APTTransactionsAPI.SUBMIT_TRANSACTION,
            params_dict=txn_dict,
            # headers=self.provider.DEFAULT_HEADERS
        )

    submit = submit_transaction

    def submit_batch_transactions(self, batch_txn_dict: dict | list):
        return self.provider.post(
            APTTransactionsAPI.SUBMIT_BATCH_TRANSACTIONS,
            params_dict=batch_txn_dict,
            # headers=self.provider.DEFAULT_HEADERS
        )

    submit_batch = submit_batch_transactions

    def simulate_transaction(
        self,
        txn_dict,
        estimate_gas_unit_price: str = "false",
        estimate_max_gas_amount: str = "false",
        estimate_prioritized_gas_unit_price: str = "false",
    ):
        j = self.provider.post(
            f"{APTTransactionsAPI.SIMULATE_TRANSACTION}"
            f"?estimate_gas_unit_price={estimate_gas_unit_price}"
            f"&estimate_max_gas_amount={estimate_max_gas_amount}"
            f"&estimate_prioritized_gas_unit_price={estimate_prioritized_gas_unit_price}",
            txn_dict,
        )
        return self._handle_simulate_error(j)

    simulate = simulate_transaction

    def encode_submission(self, txn_dict: dict):
        j = self.provider.post(
            APTTransactionsAPI.ENCODE_SUBMISSION, params_dict=txn_dict
        )
        if "message" in j:
            raise RPCRequestError(j["message"])
        else:
            return bytes.fromhex(j[2:])

    encode = encode_submission

    @staticmethod
    def _handle_simulate_error(j):
        if isinstance(j, list):
            j = j[0]
        else:
            raise ParamsError(f"Check Txn dict Params. RPC Response: {j}")

        if j["success"]:
            return j
        else:
            raise RPCRequestError(f"RPC Error: {j['vm_status']}")

    def transaction_pending(self, txn_hash: str) -> bool:
        response = self.provider.get(
            APTTransactionsAPI.GET_TRANSACTION_BY_HASH.format(txn_hash=txn_hash)
        )
        if "type" not in response:
            # unknown / not yet submitted transaction
            return True
        return response["type"] == "pending_transaction"

    def wait_for_transaction(
        self, txn_hash, timeout: int = 20, poll_interval: float = 1.0
    ) -> dict:
        """Waits up to `timeout` seconds for a transaction to move past pending state.

        Uses the `transactions/wait_by_hash` long-poll endpoint when available.
        Returns the committed transaction, raising on failure or timeout.
        """
        deadline = time.time() + timeout
        while True:
            txn = self.wait_transaction_by_hash(txn_hash)
            if "type" not in txn:
                # not found yet (e.g. just submitted), keep polling
                txn = {"type": "pending_transaction"}
            if txn["type"] != "pending_transaction":
                assert txn.get("success", False), f"{txn} - {txn_hash}"
                return txn
            if time.time() >= deadline:
                raise TimeoutError(f"transaction {txn_hash} timed out")
            time.sleep(poll_interval)


class APTDevClient(APTClient):
    def __init__(self, provider: BaseProvider):
        super().__init__(provider)
        self.provider = provider

    def deposit(self, address: Address, amount: int = 10_000_000) -> str:
        response = self.provider.client.post(
            f"{self.base_url}/mint?amount={amount}&address={address}"
        )
        if response.status_code >= 400:
            raise RPCRequestError(response.text, response.status_code)
        # for testnet it not return proper response, but still success
        return response.json()[0]
