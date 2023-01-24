from django.conf import settings
from web3 import Web3

from utils.bytecode_analyzers.bytecode_to_opcode import get_opcode
from utils.extractors.geth_node_extractor import get_contract_bin


# TODO: move this to contract_relations.link_finder
def get_attribute_links(address):
    bytecode = str(get_contract_bin(address).hex())
    instructions = get_opcode(bytecode)
    storage_locations = get_storage_locations(instructions)
    return get_addresses_in_storage(address, storage_locations)


def get_addresses_in_storage(contract_address, storage_locations):
    attribute_addresses = set()

    try:
        w3 = Web3(Web3.HTTPProvider(settings.WEB3_HTTP_PROVIDER))
    except:
        w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/abf2599d4d184669936ee3d302f8ce67'))

    for storage_location in storage_locations:
        stored_val = w3.toHex(
            w3.eth.get_storage_at(contract_address, storage_location))
        cleaned_val = clean_val(stored_val)

        if w3.isAddress(cleaned_val):
            attribute_addresses.add(cleaned_val)

    return list(attribute_addresses)


def get_storage_locations(instructions_lst):
    storage_locations = set()

    for instruction in instructions_lst:
        instruction_components = instruction.split(" ")
        instruction_type = instruction_components[2]

        if instruction_type == "PUSH32":
            try:
                storage_loc_val = instruction_components[3].split(":")[1]
            except:
                continue
            if storage_loc_val != "0xffffffffffffffffffffffffffffffffffffffff":
                storage_locations.add(storage_loc_val)

    return list(storage_locations)


def clean_val(raw_val_string):
    after_ox = raw_val_string.split("0x")[1]
    cleaned_starting_pos = 0
    for i in range(len(after_ox)):
        if after_ox[i] != "0":
            cleaned_starting_pos = i
            break

    return "0x" + after_ox[cleaned_starting_pos:]
