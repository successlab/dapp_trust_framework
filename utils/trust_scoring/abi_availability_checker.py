import requests
from django.conf import settings


def contains_abi(address):
    abi = ""

    api_endpoint = (
        f"https://api.etherscan.io/api?module=contract&action=getsourcecode"
        f"&apikey={settings.ETHERSCAN_API_KEY}&address="
    )
    response = requests.get(api_endpoint + address)

    response_json = response.json()

    abi_available, contains_source_code, contains_constructor_args = False, False, False

    try:
        abi = response_json["result"][0]["ABI"]
        source_code = response_json["result"][0]["SourceCode"]
        constructor_args = response_json["result"][0]["ConstructorArguments"]

        if abi.startswith("["):
            abi_available = True

        if source_code != "":
            contains_source_code = True

        if constructor_args != "":
            contains_constructor_args = True

        return abi_available  # , contains_source_code, contains_constructor_args


    except:
        if response_json["result"] == 'Max rate limit reached':
            return contains_abi(address)
        else:
            return False  # , False, False
