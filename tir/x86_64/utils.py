from enum import IntEnum
from elfgenerator.Binary import Binary
from functools import wraps
def modrm(mod: int, r: int, m: int):
    """Intel Volume 2A 2-6
    
    r changes row
    m changes column
    Not sure which way it's meant to be as long as you're consistent works."""
    mod = mod*2**6
    m = m*2**3
    return mod+r+m

def syscall():
    return Binary(0x050F, 2, 2), "syscall"

class Registers_Syscall_Linux_32(IntEnum):
    """
    Provides the order a 64 bit Linux syscall expects it's arguments for instructions expecting 32 bit operands.
    Note that EAX is used to determine which syscall is triggered. 
    So your parameters for the syscall start from 1-6"""
    EAX = 0
    EDI = 1
    ESI = 2
    EDX = 3
    R10D = 4
    R8D = 5
    R9D = 6

class Registers_Syscall_Linux_64(IntEnum):
    """
    Provides the order a 64 bit Linux syscall expects it's arguments for instructions expecting 64 bit operands.
    Note that EAX is used to determine which syscall is triggered. 
    So your parameters for the syscall start from 1-6"""
    RAX = 0
    RDI = 1
    RSI = 2
    RDX = 3
    R10 = 4
    R8 = 5
    R9 = 6

class Registers_32(IntEnum):
    """Order of Registers by integer in 64 bit mode x68-64 for instructions using 32 bit operands"""
    EAX = 0
    ECX = 1
    EDX = 2
    EBX = 3
    ESP = 4
    EBP = 5
    ESI = 6
    EDI = 7
    R8D = 8
    R9D = 9
    R10D = 10
    R11D = 11
    R12D = 12
    R13D = 13
    R14D = 14
    R15D = 15

class Registers_64(IntEnum):
    """Order of Registers by integer in 64 bit mode x68-64 for instructions using 64 bit operands"""
    RAX = 0
    RCX = 1
    RDX = 2
    RBX = 3
    RSP = 4
    RBP = 5
    RSI = 6
    RDI = 7
    R8 = 8
    R9 = 9
    R10 = 10
    R11 = 11
    R12 = 12
    R13 = 13
    R14 = 14
    R15 = 15


def bits_validator(func):
    @wraps(func)
    def kernel(*args, **kwargs):
        bits = args[-1]
        if(bits not in (8, 16, 32, 64)):
            return ValueError("bits must be 8, 16, 32 or 64 bits")
        if(bits in (8, 16)):
            raise NotImplementedError()
        return func(*args, **kwargs)
    return kernel

def _binary_op_string_adder(op: str, str1: str, str2: str):
    return op + " " + str1 + ", " + str2

def _unary_op_string_adder(op: str , str1: str):
    return op + " " + str1

@bits_validator
def binary_instruction_rr(asm_instruction: str, reg_1: int, reg_2: int, bits: int):
    if(bits == 32):
        return _binary_op_string_adder(asm_instruction, Registers_32(reg_1).name, Registers_32(reg_2).name)
    elif(bits == 64):
        return _binary_op_string_adder(asm_instruction, Registers_64(reg_1).name, Registers_64(reg_2).name)

@bits_validator
def unary_instruction_r(asm_instruction: str, reg: int, bits: int):
    if(bits == 32):
        return _unary_op_string_adder(asm_instruction, Registers_32(reg).name)
    elif(bits == 64):
        return _unary_op_string_adder(asm_instruction, Registers_64(reg).name)

@bits_validator
def binary_instruction_cr(asm_instruction: str, reg_1: int, const: int, bits: int):
    if(bits == 32):
        return _binary_op_string_adder(asm_instruction, Registers_32(reg_1).name, str(const))
    elif(bits == 64):
        return _binary_op_string_adder(asm_instruction, Registers_64(reg_1).name, str(const))

@bits_validator
def binary_instruction_mr(asm_instruction: str, value_to_memory: int, reg: int, bits: int):
    if(bits == 32):
        return _binary_op_string_adder(asm_instruction, Registers_32(reg).name, f"[{value_to_memory}]")
    elif(bits == 64):
        return _binary_op_string_adder(asm_instruction, Registers_64(reg).name, f"[{value_to_memory}]")

@bits_validator
def binary_instruction_rm(asm_instruction: str, reg: int, memory_address: int, bits: int):
    if(bits == 32):
        return _binary_op_string_adder(asm_instruction, f"[{memory_address}]", Registers_32(reg).name)
    elif(bits == 64):
        return _binary_op_string_adder(asm_instruction, f"[{memory_address}]", Registers_64(reg).name)

