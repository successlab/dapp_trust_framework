import requests
import json


def get_contract_props_from_etherscan(address):
    ABI_ENDPOINT = (
        "https://api.etherscan.io/api?module=contract&action=getsourcecode&address="
    )
    response = requests.get(ABI_ENDPOINT + address)
    response_json = response.json()

    source_code = response_json["SourceCode"]
    abi = json.loads(response_json["ABI"])
    is_proxy = response_json["Proxy"] == "1"

    return source_code, abi, is_proxy
