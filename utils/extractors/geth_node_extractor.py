from django.conf import settings
from web3 import Web3


def get_contract_bin(address):
    try:
        w3 = Web3(Web3.HTTPProvider(settings.WEB3_HTTP_PROVIDER))
    except:
        w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/abf2599d4d184669936ee3d302f8ce67'))
    bin = w3.eth.get_code(address)
    return bin
