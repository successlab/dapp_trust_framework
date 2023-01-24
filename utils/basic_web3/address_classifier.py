from django.conf import settings
from hexbytes import HexBytes
from web3 import Web3


def is_contract(address):
    w3 = Web3(Web3.HTTPProvider(settings.WEB3_HTTP_PROVIDER))
    address = w3.toChecksumAddress(address)
    contract_code = w3.eth.get_code(address)
    if contract_code == HexBytes('0x'):
        return False
    else:
        return True


def is_valid_eth_address(address):
    w3 = Web3(Web3.HTTPProvider(settings.WEB3_HTTP_PROVIDER))
    address = w3.toChecksumAddress(address)
    if w3.isAddress(address):
        return True
    else:
        return False
