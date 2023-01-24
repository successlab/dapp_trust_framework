import json

import requests


def get_all_contract_props(address):
    api_endpoint = (
        "https://api.etherscan.io/api?module=contract&action=getsourcecode&address="
    )
    response = requests.get(api_endpoint + address)
    response_json = response.json()

    source_code = response_json["SourceCode"]
    abi = json.loads(response_json["ABI"])
    is_proxy = response_json["Proxy"] == "1"

    return source_code, abi, is_proxy


def get_contract_abi(address):
    api_endpoint = (
        "https://api.etherscan.io/api?module=contract&action=getsourcecode&address="
    )
    response = requests.get(api_endpoint + address)
    response_json = response.json()
    abi = response_json["result"][0]["ABI"]

    return abi
