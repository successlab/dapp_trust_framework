import json
from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.conf import settings

import requests


def get_all_contract_props(address):
    api_endpoint = (
        f"https://api.etherscan.io/api?module=contract&action=getsourcecode&address={address}"
        f"&apikey={settings.ETHERSCAN_API_KEY}"
    )
    response = requests.get(api_endpoint)
    response_json = response.json()

    if response_json['message'] == "OK":
        try:
            response_json = response_json["result"][0]
        except:
            return None, None, False, None

        try:
            source_code = response_json["SourceCode"]
        except:
            source_code = ""

        try:
            abi = json.loads(response_json["ABI"])
        except:
            abi = None

        try:
            is_proxy = response_json["Proxy"] == "1"
        except:
            is_proxy = False

        try:
            contract_name = response_json["ContractName"]
        except:
            contract_name = None

        return source_code, abi, is_proxy, contract_name

    else:
        return None, None, None, None


def get_contract_abi(address):
    api_endpoint = (
        f"https://api.etherscan.io/api?module=contract&action=getsourcecode&apikey={settings.ETHERSCAN_API_KEY}&address="
    )
    response = requests.get(api_endpoint + address)

    try:
        response_json = response.json()
    except:
        return ""

    try:
        abi = response_json["result"][0]["ABI"]
        return abi
    except:
        if response_json["result"] == 'Max rate limit reached':
            return get_contract_abi(address)
        else:
            return ""


def get_all_transactions_until_limit(address, n_months):
    api_call = "https://api.etherscan.io/api?module=account&action=txlist&address=" + address + "&apikey=" + \
               settings.ETHERSCAN_API_KEY
    response = requests.get(api_call).json()

    if response["status"] != "1":
        raise Exception("Error in making an API call to get the transactions for account: " + address)

    transaction_list = response["result"]
    initial_dt_timestamp = int(transaction_list[0]['timeStamp'])
    initial_dt = datetime.fromtimestamp(initial_dt_timestamp)
    last_dt = initial_dt + relativedelta(months=n_months)
    timestamp_limit = int(datetime.timestamp(last_dt))

    n_transactions = len(transaction_list)
    last_tx = transaction_list[-1]
    last_tx_ts = int(last_tx['timeStamp'])

    # Fetching more for high frequency contracts
    while n_transactions >= 10000 and last_tx_ts < timestamp_limit:
        api_call = "https://api.etherscan.io/api?module=account&action=txlist&address=" + address + "&apikey=" + \
                   settings.ETHERSCAN_API_KEY + "&startblock=" + \
                   last_tx['blockNumber']
        response = requests.get(api_call).json()

        if response["status"] != "1":
            # print("Error in making an API call to get the transactions for account: " + address)
            # return
            # raise Exception("Error in making an API call to get the transactions for account: " + address)
            break

        elif len(response["result"]) == 0:
            break

        else:
            transaction_list = transaction_list + response["result"]
            n_transactions = len(transaction_list)
            last_tx = transaction_list[-1]
            last_tx_ts = int(last_tx['timeStamp'])

    final_result = list(filter(lambda x: int(x['timeStamp']) <= timestamp_limit, transaction_list))

    return final_result
