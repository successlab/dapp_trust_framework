from utils.bytecode_analyzers.bytecode_to_opcode import get_opcode
from utils.bytecode_analyzers.opcode_analyzer import get_external_addresses
from utils.extractors.geth_node_extractor import get_contract_bin
from utils.extractors.etherscan_extractor import get_contract_abi

def get_code_links(address):
    bytecode = get_contract_bin(address)
    opcode_instructions = get_opcode(bytecode).hex()
    code_link_addresses = get_external_addresses(opcode_instructions)
    return list(code_link_addresses)

def get_attribute_links(address):
    abi = get_contract_abi(address)

    #TODO: Use the public variables/attributes with addresses
    pass