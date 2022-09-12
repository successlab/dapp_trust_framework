def get_external_addresses(opcodes_lst):
    external_addresses = set()

    for instruction in opcodes_lst:
        instruction_components = instruction.split(" ")
        instruction_type = instruction_components[2]

        if instruction_type == "PUSH20":
            address_val = instruction_components[3].split(":")[1]
            if address_val != "0xffffffffffffffffffffffffffffffffffffffff":
                external_addresses.add(address_val)

    return external_addresses
