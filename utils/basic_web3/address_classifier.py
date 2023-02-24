from django.conf import settings
from hexbytes import HexBytes
from web3 import Web3

from contract_relations.submodels.contract_models import Address
from utils.extractors.etherscan_extractor import get_contract_abi


def is_contract(address):

    try:
        if Address.objects.filter(eth_address=address).exists():
            address_obj = Address.objects.get(eth_address=address)

            if address_obj.type.lower() == "contract":
                return True

            else:
                return False
    except:
        pass

    w3 = Web3(Web3.HTTPProvider(settings.WEB3_HTTP_PROVIDER))
    address = w3.toChecksumAddress(address)
    if is_null_address(address):
        return True

    contract_code = w3.eth.get_code(address)
    abi = get_contract_abi(address)

    if (abi != "" and abi != "Contract source code not verified" and abi.startswith("[")) or contract_code != HexBytes(
            '0x'):
        return True
    else:
        return False


def is_valid_eth_address(address):
    w3 = Web3(Web3.HTTPProvider(settings.WEB3_HTTP_PROVIDER))
    address = w3.toChecksumAddress(address)
    if w3.isAddress(address):
        return True
    else:
        return False


def is_null_address(address):
    # Source: https://etherscan.io/accounts/label/burn
    null_addresses = {
        ("0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE").lower(): True,
        ("0xfeEFEEfeefEeFeefEEFEEfEeFeefEEFeeFEEFEeF").lower(): True,
        "0x000000000000000000000000000000000000dead": True,
        "0x0000000000000000000000000000000000000000": True,
        "0x0000000000000000000000000000000000000001": True,
        "0x0000000000000000000000000000000000000002": True,
        "0x0000000000000000000000000000000000000003": True,
        "0x0000000000000000000000000000000000000004": True,
        "0x0000000000000000000000000000000000000005": True,
        "0x0000000000000000000000000000000000000006": True,
        "0x0000000000000000000000000000000000000007": True,
        "0x0000000000000000000000000000000000000008": True,
        "0x0000000000000000000000000000000000000009": True,
        "0x00000000000000000000045261d4ee77acdb3286": True,
        "0x0123456789012345678901234567890123456789": True,
        "0x1111111111111111111111111111111111111111": True,
        "0x1234567890123456789012345678901234567890": True,
        "0x2222222222222222222222222222222222222222": True,
        "0x3333333333333333333333333333333333333333": True,
        "0x4444444444444444444444444444444444444444": True,
        "0x6666666666666666666666666666666666666666": True,
        "0x8888888888888888888888888888888888888888": True,
        "0xbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb": True,
        "0xdead000000000000000042069420694206942069": True,
        "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa": True,
    }

    if address.lower() in null_addresses:
        return True
    else:
        return False