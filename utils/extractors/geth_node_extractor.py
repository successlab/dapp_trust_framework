from web3 import Web3
from django.conf import settings


def get_contract_bin(address):
    w3 = Web3(Web3.HTTPProvider(settings.WEB3_HTTP_PROVIDER))
    bin = w3.eth.get_code(address)
    return bin
