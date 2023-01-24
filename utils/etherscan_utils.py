import json

import requests
from django.conf import settings
from web3 import Web3


def fetch_abi(contract_address):
    # Connect to an Ethereum node
    web3 = Web3(Web3.HTTPProvider(settings.WEB3_HTTP_PROVIDER))

    # Fetch the ABI from Etherscan
    url = f"https://api.etherscan.io/api?module=contract&action=getabi&address={contract_address}&apikey={settings.ETHERSCAN_API_KEY}"
    response = requests.get(url)
    abi = response.json()['result']

    # Decode the ABI
    abi = json.loads(abi)

    return abi
