from elfgenerator.Binary import Binary

from enum import IntEnum
from tir.x86_64.utils import *

"""All the following classes and static methods should return a Binary object and a String
 Operations are left to right as opposed to Intel asm which is right to left"""

class Int32():
    """All operations that work with 32 bit Integers"""

    @staticmethod
    def signed_multiply_register_one_with_register_two(reg1: int, reg2: int) -> tuple[Binary, str]:
        text = binary_instruction_rr("IMUL", reg1, reg2, 32)
        opcode = Binary(0x0f, 1, 1)
        opcode += Binary(0xaf, 1, 1)
        upper_64_prefix = Binary(0, 0, 0)
        if(reg1 >= 8):
            upper_64_prefix = Binary(0x41, 1, 1)
            reg1 -= 8
        if(reg2 >= 8):
            upper_64_prefix = Binary(0x44, 1, 1)
            reg2 -= 8
        if(reg1 >= 8 and reg2 >= 8):
            upper_64_prefix = Binary(0x45, 1, 1)
        register_pair = modrm(3, reg1, reg2)
        register_pair = Binary(register_pair, 1, 1)
        binary = upper_64_prefix + opcode + register_pair
        return binary, text
    
    @staticmethod
    def subtract_register_one_with_register_two(reg1: int, reg2: int) -> tuple[Binary, str]:
        text = binary_instruction_rr("SUB", reg1, reg2, 32)
        opcode = Binary(0x29, 1, 1)
        upper_64_prefix = Binary(0, 0, 0)
        if(reg1 >= 8):
            upper_64_prefix = Binary(0x41, 1, 1)
            reg1 -= 8
        if(reg2 >= 8):
            upper_64_prefix = Binary(0x44, 1, 1)
            reg2 -= 8
        if(reg1 >= 8 and reg2 >= 8):
            upper_64_prefix = Binary(0x45, 1, 1)
        register_pair = modrm(3, reg1, reg2)
        register_pair = Binary(register_pair, 1, 1)
        binary = upper_64_prefix + opcode + register_pair
        return binary, text
    
    @staticmethod
    def add_register_one_with_register_two(reg1: int, reg2: int) -> tuple[Binary, str]:
        text = binary_instruction_rr("ADD", reg1, reg2, 32)
        opcode = Binary(1, 1, 1)
        upper_64_prefix = Binary(0, 0, 0)
        if(reg1 >= 8):
            upper_64_prefix = Binary(0x41, 1, 1)
            reg1 -= 8
        if(reg2 >= 8):
            upper_64_prefix = Binary(0x44, 1, 1)
            reg2 -= 8
        if(reg1 >= 8 and reg2 >= 8):
            upper_64_prefix = Binary(0x45, 1, 1)
        register_pair = modrm(3, reg1, reg2)
        register_pair = Binary(register_pair, 1, 1)
        binary = upper_64_prefix + opcode + register_pair
        return binary, text

    @staticmethod
    def load_const_to_register_displacement_only(register: int, constant: int) -> tuple[Binary, str]:
        text = binary_instruction_cr("MOV", register, constant, 32)
        binary = Binary(0,0,0)
        if(register >= 8):
            binary = Binary(0x41, 1, 1)
            register -= 8
        binary += Binary(modrm(2, register, 7), 1, 1) + Binary(constant, 4, 4)
        return binary, text

    @staticmethod
    def load_memory_value_to_register_displacement_only(register: int, address: int) -> tuple[Binary, str]:
        text = binary_instruction_mr("MOV", address, register, 32)
        if(register >= 8):
            pre_prefix = Binary(0x44, 1, 1)
            register -= 8
        else:
            pre_prefix = Binary(0,0,0)
        prefix = Binary(0x8b, 1, 1)
        value = modrm(0, 4, register)
        reg = Binary(value, 1, 1)
        suffix = Binary(0x25, 1, 1)
        address = Binary(address, 4, 4)
        binary = pre_prefix + prefix + reg + suffix + address 
        return binary, text

    @staticmethod
    def load_register_value_to_memory_address_displacement_only(register: int, address: int) -> tuple[Binary, str]:
        text = binary_instruction_rm("MOV", register, address, 32)
        if(register >= 8):
            pre_prefix = Binary(0x44, 1, 1)
            register -= 8
        else:
            pre_prefix = Binary(0,0,0)
        prefix = Binary(0x89, 1, 1)
        value = modrm(0, 4, register)
        reg = Binary(value, 1, 1)
        suffix = Binary(0x25, 1, 1)
        address = Binary(address, 4, 4)
        binary = pre_prefix + prefix + reg + suffix + address 
        return binary, text

