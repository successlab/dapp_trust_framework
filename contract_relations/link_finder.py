from utils.bytecode_analyzers.bytecode_to_opcode import get_opcode
from utils.bytecode_analyzers.opcode_analyzer import get_external_addresses_in_code
from utils.bytecode_analyzers.stored_address_vals import get_storage_locations, get_addresses_in_storage
from utils.extractors.geth_node_extractor import get_contract_bin


def get_code_links(address):
    bytecode = str(get_contract_bin(address).hex())
    opcode_instructions = get_opcode(bytecode)
    code_link_addresses = get_external_addresses_in_code(opcode_instructions)
    return list(code_link_addresses)


def get_attribute_links(address):
    bytecode = str(get_contract_bin(address).hex())
    instructions = get_opcode(bytecode)
    storage_locations = get_storage_locations(instructions)
    return get_addresses_in_storage(address, storage_locations)
