from utils.bytecode_analyzers.bytecode_to_opcode import get_opcode
from utils.bytecode_analyzers.stored_address_vals import get_attribute_links
from utils.extractors.geth_node_extractor import get_contract_bin


def get_external_addresses_in_code(instructions_lst):
    """
    :param instructions_lst: list of opcodes (like the one returned by get_opcode in
                                utils.bytecode_analyzers.bytecode_to_opcode

    :return: A set of external addresses referred in the contract
    """
    external_addresses = set()

    for instruction in instructions_lst:
        instruction_components = instruction.split(" ")
        instruction_type = instruction_components[2]

        if instruction_type == "PUSH20":
            try:
                address_val = instruction_components[3].split(":")[1]
            except:
                continue
            if address_val != "0xffffffffffffffffffffffffffffffffffffffff":
                external_addresses.add(address_val)

    return external_addresses


if __name__ == "__main__":
    address = '0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9'
    bytecode = str(get_contract_bin(address).hex())
    instructions = get_opcode(bytecode)
    external_addresses = get_external_addresses_in_code(instructions)
    print("\nAddresses explicitly defined in code: ", external_addresses)
    print("\nAddresses pointed by the attributes in the contract: ", get_attribute_links(address))
