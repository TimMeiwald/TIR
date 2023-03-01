from elfgenerator.Binary import Binary

from enum import IntEnum
from tir.x86_64.utils import modrm, syscall

"""All the following classes and static methods should return a Binary object and a String"""
class Int32():
    """All operations that work with 32 bit Integers"""

    @staticmethod
    def signed_multiply_register_one_with_register_two(reg1: int, reg2: int) -> tuple(Binary, str):
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
        return upper_64_prefix + opcode + register_pair
    
    @staticmethod
    def subtract_register_one_with_register_two(reg1: int, reg2: int) -> tuple(Binary, str):
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
        return upper_64_prefix + opcode + register_pair
    
    @staticmethod
    def add_register_one_with_register_two(reg1: int, reg2: int) -> tuple(Binary, str):
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
        return upper_64_prefix + opcode + register_pair



    @staticmethod
    def load_const_to_register_displacement_only(register: int, constant) -> tuple(Binary, str):
        binary = Binary(0,0,0)
        if(register >= 8):
            binary = Binary(0x41, 1, 1)
            register -= 8
        binary += Binary(modrm(2, register, 7), 1, 1) + Binary(constant, 4, 4)
        return binary

    @staticmethod
    def load_memory_value_to_register_displacement_only(register: int, address) -> tuple(Binary, str):
        if(register >= 8):
            pre_prefix = Binary(0x44, 1, 1)
            register -= 8
        else:
            pre_prefix = Binary(0,0,0)
        prefix = Binary(0x8b, 1, 1)
        value = modrm(0, 4, register)
        register = Binary(value, 1, 1)
        suffix = Binary(0x25, 1, 1)
        address = Binary(address, 4, 4)
        return pre_prefix + prefix + register + suffix + address 

    @staticmethod
    def load_register_value_to_memory_address_displacement_only(register: int, address) -> tuple(Binary, str):
        if(register >= 8):
            pre_prefix = Binary(0x44, 1, 1)
            register -= 8
        else:
            pre_prefix = Binary(0,0,0)
        prefix = Binary(0x89, 1, 1)
        value = modrm(0, 4, register)
        register = Binary(value, 1, 1)
        suffix = Binary(0x25, 1, 1)
        address = Binary(address, 4, 4)
        return pre_prefix + prefix + register + suffix + address 


