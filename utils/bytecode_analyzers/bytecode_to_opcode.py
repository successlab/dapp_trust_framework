import sys

# Original Github author: https://github.com/daejunpark/
# Github repo link: https://github.com/daejunpark/evm-disassembler

opcodes = {
    "00": "STOP",
    "01": "ADD",
    "02": "MUL",
    "03": "SUB",
    "04": "DIV",
    "05": "SDIV",
    "06": "MOD",
    "07": "SMOD",
    "08": "ADDMOD",
    "09": "MULMOD",
    "0a": "EXP",
    "0b": "SIGNEXTEND",
    "10": "LT",
    "11": "GT",
    "12": "SLT",
    "13": "SGT",
    "14": "EQ",
    "15": "ISZERO",
    "16": "AND",
    "17": "OR",  # 'EVMOR'
    "18": "XOR",
    "19": "NOT",
    "1a": "BYTE",
    "1b": "SHL",
    "1c": "SHR",
    "1d": "SAR",
    "20": "SHA3",
    "30": "ADDRESS",
    "31": "BALANCE",
    "32": "ORIGIN",
    "33": "CALLER",
    "34": "CALLVALUE",
    "35": "CALLDATALOAD",
    "36": "CALLDATASIZE",
    "37": "CALLDATACOPY",
    "38": "CODESIZE",
    "39": "CODECOPY",
    "3a": "GASPRICE",
    "3b": "EXTCODESIZE",
    "3c": "EXTCODECOPY",
    "3d": "RETURNDATASIZE",
    "3e": "RETURNDATACOPY",
    "3f": "EXTCODEHASH",
    "40": "BLOCKHASH",
    "41": "COINBASE",
    "42": "TIMESTAMP",
    "43": "NUMBER",
    "44": "DIFFICULTY",
    "45": "GASLIMIT",
    "50": "POP",
    "51": "MLOAD",
    "52": "MSTORE",
    "53": "MSTORE8",
    "54": "SLOAD",
    "55": "SSTORE",
    "56": "JUMP",
    "57": "JUMPI",
    "58": "PC",
    "59": "MSIZE",
    "5a": "GAS",
    "5b": "JUMPDEST",
    "60": "PUSH1",
    "61": "PUSH2",
    "62": "PUSH3",
    "63": "PUSH4",
    "64": "PUSH5",
    "65": "PUSH6",
    "66": "PUSH7",
    "67": "PUSH8",
    "68": "PUSH9",
    "69": "PUSH10",
    "6a": "PUSH11",
    "6b": "PUSH12",
    "6c": "PUSH13",
    "6d": "PUSH14",
    "6e": "PUSH15",
    "6f": "PUSH16",
    "70": "PUSH17",
    "71": "PUSH18",
    "72": "PUSH19",
    "73": "PUSH20",
    "74": "PUSH21",
    "75": "PUSH22",
    "76": "PUSH23",
    "77": "PUSH24",
    "78": "PUSH25",
    "79": "PUSH26",
    "7a": "PUSH27",
    "7b": "PUSH28",
    "7c": "PUSH29",
    "7d": "PUSH30",
    "7e": "PUSH31",
    "7f": "PUSH32",
    "80": "DUP1",
    "81": "DUP2",
    "82": "DUP3",
    "83": "DUP4",
    "84": "DUP5",
    "85": "DUP6",
    "86": "DUP7",
    "87": "DUP8",
    "88": "DUP9",
    "89": "DUP10",
    "8a": "DUP11",
    "8b": "DUP12",
    "8c": "DUP13",
    "8d": "DUP14",
    "8e": "DUP15",
    "8f": "DUP16",
    "90": "SWAP1",
    "91": "SWAP2",
    "92": "SWAP3",
    "93": "SWAP4",
    "94": "SWAP5",
    "95": "SWAP6",
    "96": "SWAP7",
    "97": "SWAP8",
    "98": "SWAP9",
    "99": "SWAP10",
    "9a": "SWAP11",
    "9b": "SWAP12",
    "9c": "SWAP13",
    "9d": "SWAP14",
    "9e": "SWAP15",
    "9f": "SWAP16",
    "a0": "LOG0",
    "a1": "LOG1",
    "a2": "LOG2",
    "a3": "LOG3",
    "a4": "LOG4",
    "f0": "CREATE",
    "f1": "CALL",
    "f2": "CALLCODE",
    "f3": "RETURN",
    "f4": "DELEGATECALL",
    "f5": "CREATE2",
    "fa": "STATICCALL",
    "fd": "REVERT",
    "fe": "INVALID",
    "ff": "SELFDESTRUCT",
    #   'ff' : 'SUICIDE',
}


def push_bytes(h, mode):
    i = str(int(h, 16))
    return {
        "hex": "0x" + h,
        "int": i,
        "int:hex": i + ":" + "0x" + h,
    }[mode]


def pc(cnt, size):
    return "[" + str(cnt).zfill(size) + "]"


# Decode ByteCodes to Opcodes
def decode(hexcode, mode):
    size = len(str(len(hexcode)))
    h = ""
    o = ""
    pushcnt = 0
    cnt = -1
    for item in hexcode:
        cnt += 1
        if pushcnt > 0:
            h += item.lower()
            pushcnt -= 1
            if pushcnt == 0:
                i = str(int(h, 16))
                o += push_bytes(h, mode) + "\n"
                h = ""
        elif isinstance(item, str) and item.lower() in opcodes:
            o += pc(cnt, size) + " " + item.lower() + " " + opcodes[item.lower()]
            if int("60", 16) <= int(item, 16) <= int("7f", 16):
                pushcnt = int(item, 16) - int("60", 16) + 1
                o += " "
            else:
                o += "\n"
        else:
            o += pc(cnt, size) + " " + item.lower() + " ERROR\n"
    #           raise Exception("Invalid opcode: " + str(item))
    if h:
        o += "ERROR " + push_bytes(h, mode) + " (" + str(pushcnt) + " bytes missed)\n"
    #       raise Exception("Not enough push bytes: " + h)
    return o.strip()


# THIS IS THE MAIN FUNCTION
def get_opcode(bytecode):
    mode = "int:hex"  # if len(sys.argv) < 2 else sys.argv[1]
    hexcode = bytecode
    opcodes_str = decode([hexcode[i: i + 2] for i in range(2, len(hexcode), 2)], mode)
    opcodes_lst = opcodes_str.split("\n")
    return opcodes_lst


# # usage: <cmd> [int|hex|int:hex]
# if __name__ == '__main__':
#     mode = 'int:hex' if len(sys.argv) < 2 else sys.argv[1]
#     hexcode = input()
#     print(decode([hexcode[i:i + 2] for i in range(2, len(hexcode), 2)], mode))

if __name__ == "__main__":
    bytecode = "608060405234801561001057600080fd5b506000735f4ec3df9cbd43714fe2740f5e3616155c5b84199050600073f4030086522a5beea4988f8ca5b36dbc97bee88c905081600360006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555033600260006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055505050610939806100d66000396000f3fe6080604052600436106100915760003560e01c8063741bef1a11610059578063741bef1a146101aa5780638da5cb5b146101eb57806398d5fdca1461022c578063b60d428814610257578063dc0d3dff1461026157610091565b806309bc33a7146100965780630d8e6e2c146100c15780633ccfd60b146100ec5780633e47d6f3146100f65780636e5b6b281461015b575b600080fd5b3480156100a257600080fd5b506100ab6102c6565b6040518082815260200191505060405180910390f35b3480156100cd57600080fd5b506100d6610305565b6040518082815260200191505060405180910390f35b6100f46103af565b005b34801561010257600080fd5b506101456004803603602081101561011957600080fd5b81019080803573ffffffffffffffffffffffffffffffffffffffff16906020019092919050505061054f565b6040518082815260200191505060405180910390f35b34801561016757600080fd5b506101946004803603602081101561017e57600080fd5b8101908080359060200190929190505050610567565b6040518082815260200191505060405180910390f35b3480156101b657600080fd5b506101bf610596565b604051808273ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b3480156101f757600080fd5b506102006105bc565b604051808273ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b34801561023857600080fd5b506102416105e2565b6040518082815260200191505060405180910390f35b61025f6106c4565b005b34801561026d57600080fd5b5061029a6004803603602081101561028457600080fd5b8101908080359060200190929190505050610802565b604051808273ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b6000806802b5e3af16b1880000905060006102df6105e2565b90506000670de0b6b3a76400009050600182828502816102fb57fe5b0401935050505090565b6000600360009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff166354fd4d506040518163ffffffff1660e01b815260040160206040518083038186803b15801561036f57600080fd5b505afa158015610383573d6000803e3d6000fd5b505050506040513d602081101561039957600080fd5b8101908080519060200190929190505050905090565b600260009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff161461040957600080fd5b3373ffffffffffffffffffffffffffffffffffffffff166108fc479081150290604051600060405180830381858888f1935050505015801561044f573d6000803e3d6000fd5b5060005b6001805490508110156104ee5760006001828154811061046f57fe5b9060005260206000200160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff16905060008060008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002081905550508080600101915050610453565b50600067ffffffffffffffff8111801561050757600080fd5b506040519080825280602002602001820160405280156105365781602001602082028036833780820191505090505b506001908051906020019061054c92919061083e565b50565b60006020528060005260406000206000915090505481565b6000806105726105e2565b90506000670de0b6b3a76400008483028161058957fe5b0490508092505050919050565b600360009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b600260009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b600080600360009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1663feaf968c6040518163ffffffff1660e01b815260040160a06040518083038186803b15801561064d57600080fd5b505afa158015610661573d6000803e3d6000fd5b505050506040513d60a081101561067757600080fd5b8101908080519060200190929190805190602001909291908051906020019092919080519060200190929190805190602001909291905050505050509150506402540be400810291505090565b60006802b5e3af16b18800009050806106dc34610567565b1015610750576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040180806020018281038252601b8152602001807f596f75206e65656420746f207370656e64206d6f72652045544821000000000081525060200191505060405180910390fd5b346000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600082825401925050819055506001339080600181540180825580915050600190039060005260206000200160009091909190916101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555050565b6001818154811061080f57fe5b906000526020600020016000915054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b8280548282559060005260206000209081019282156108b7579160200282015b828111156108b65782518260006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055509160200191906001019061085e565b5b5090506108c491906108c8565b5090565b5b808211156108ff57600081816101000a81549073ffffffffffffffffffffffffffffffffffffffff0219169055506001016108c9565b509056fea26469706673582212206d3199971d26c263b5bf9f22d583b6dab79ce675856bde1cb8b09c79e56f0da864736f6c634300060c0033"
    print(get_opcode(bytecode))
