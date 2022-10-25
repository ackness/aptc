class APTAccountAPI:
    # common api
    GET_ACCOUNT = "accounts/{address}"
    GET_ACCOUNT_RESOURCES = "accounts/{address}/resources"
    GET_ACCOUNT_RESOURCE = "accounts/{address}/resource/{resource_type}"
    GET_ACCOUNT_MODULES = "accounts/{address}/modules"
    GET_ACCOUNT_MODULE = "accounts/{address}/modules/{module_name}"

    # specific api
    GET_ACCOUNT_BALANCE = "accounts/{address}/resource/0x1::coin::CoinStore<0x1::aptos_coin::AptosCoin>"


class APTBlockAPI:
    GET_BLOCK_BY_HEIGHT = "blocks/by_height/{block_height}"
    GET_BLOCK_BY_VERSION = "blocks/by_version/{version}"


class APTEventAPI:
    GET_EVENT_BY_CREATION_NUMBER = "accounts/{address}/events/{creation_number}"
    GET_EVENT_BY_EVENT_HANDLE = "accounts/{address}/events/{event_handle}/{field_name}"


class APTGeneralAPI:
    SHOW_OPENAPI_EXPLORER = "spec"
    CHECK_NODE_HEALTH = '-/healthy'
    GET_LEDGER_INFO = ""


class APTTablesAPI:
    GET_TABLE_ITEM = "tables/{table_handle}/item"


class APTTransactionsAPI:
    GET_TRANSACTIONS = "transactions"  # GET
    SUBMIT_TRANSACTION = "transactions"  # POST
    GET_TRANSACTION_BY_HASH = "transactions/by_hash/{txn_hash}"
    GET_TRANSACTION_BY_VERSION = "transactions/by_version/{txn_version}"
    GET_ACCOUNT_TRANSACTIONS = "accounts/{address}/transactions"
    SUBMIT_BATCH_TRANSACTIONS = "transactions/batch"  # POST
    SIMULATE_TRANSACTION = "transactions/simulate"  # POST
    ENCODE_SUBMISSION = "transactions/encode_submission"  # POST
    ESTIMATE_GAS_PRICE = "estimate_gas_price"
