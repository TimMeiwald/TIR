from elfgenerator.Binary import Binary
from enum import IntEnum

"""All the following classes and static methods should return a Binary object and a String
 Operations are left to right as opposed to Intel asm which is right to left"""

class Int32():
    """All operations that work with 32 bit Integers"""

    @staticmethod
    def _calculate_prefix(*, reg1: int = 0, reg2: int = 0):
        """Calculates the prefix byte required when 32 bit uses a register
        greater than Register 7. Aka the registers added in x86-64 instead of just the ones
        used in x86."""
        upper_64_prefix = Binary(0, 0, 0)
        if(reg1 >= 8):
            upper_64_prefix = Binary(0x41, 1, 1)
        if(reg2 >= 8):
            upper_64_prefix = Binary(0x44, 1, 1)
        if(reg1 >= 8 and reg2 >= 8):
            upper_64_prefix = Binary(0x45, 1, 1)
        return upper_64_prefix
    
    @staticmethod
    def signed_multiply_register_one_with_register_two(reg1: int, reg2: int) -> tuple[Binary, str]:
        text = binary_instruction_rr("IMUL", reg1, reg2, 32)
        opcode = Binary(0x0f, 1, 1)
        opcode += Binary(0xaf, 1, 1)
        upper_64_prefix = Int32._calculate_prefix(reg1=reg1, reg2=reg2)
        register_pair = modrm(3, reg2, reg1)
        register_pair = Binary(register_pair, 1, 1)
        binary = upper_64_prefix + opcode + register_pair
        return binary, text
    
    @staticmethod
    def subtract_register_one_with_register_two(reg1: int, reg2: int) -> tuple[Binary, str]:
        text = binary_instruction_rr("SUB", reg1, reg2, 32)
        opcode = Binary(0x29, 1, 1)
        upper_64_prefix = Int32._calculate_prefix(reg1=reg1, reg2=reg2)
        register_pair = modrm(3, reg1, reg2)
        register_pair = Binary(register_pair, 1, 1)
        binary = upper_64_prefix + opcode + register_pair
        return binary, text
    
    @staticmethod
    def add_register_one_with_register_two(reg1: int, reg2: int) -> tuple[Binary, str]:
        text = binary_instruction_rr("ADD", reg1, reg2, 32)
        opcode = Binary(1, 1, 1)
        upper_64_prefix = Int32._calculate_prefix(reg1=reg1, reg2=reg2)
        register_pair = modrm(3, reg1, reg2)
        register_pair = Binary(register_pair, 1, 1)
        binary = upper_64_prefix + opcode + register_pair
        return binary, text

    @staticmethod
    def udiv_register_one_with_register_two(reg: int) -> tuple[Binary, str]:
        """Unsigned Quotient in EAX, Remainder in EDX"""
        text = unary_instruction_r("DIV", reg, 32)
        opcode = Binary(0xF7, 1, 1)
        upper_64_prefix = Int32._calculate_prefix(reg1=reg)
        register_pair = modrm(3, reg, 6) 
        register_pair = Binary(register_pair, 1, 1)
        binary = upper_64_prefix + opcode + register_pair
        return binary, text

    @staticmethod
    def idiv_register_one_with_register_two(reg: int) -> tuple[Binary, str]:
        """Unsigned Quotient in EAX, Remainder in EDX"""
        text = unary_instruction_r("IDIV", reg, 32)
        opcode = Binary(0xF7, 1, 1)
        upper_64_prefix = Int32._calculate_prefix(reg1=reg)
        register_pair = modrm(3, reg, 7) 
        register_pair = Binary(register_pair, 1, 1)
        binary = upper_64_prefix + opcode + register_pair
        return binary, text

    @staticmethod
    def load_const_to_register_displacement_only(register: int, constant: int) -> tuple[Binary, str]:
        text = binary_instruction_cr("MOV", register, constant, 32)
        binary = Int32._calculate_prefix(reg1=register)
        binary += Binary(modrm(2, register, 7), 1, 1) + Binary(constant, 4, 4)
        return binary, text

    @staticmethod
    def load_memory_value_to_register_displacement_only(register: int, address: int) -> tuple[Binary, str]:
        text = binary_instruction_mr("MOV", address, register, 32)
        pre_prefix = Int32._calculate_prefix(reg1=register)
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
        pre_prefix = Int32._calculate_prefix(reg1=register)
        prefix = Binary(0x89, 1, 1)
        value = modrm(0, 4, register)
        reg = Binary(value, 1, 1)
        suffix = Binary(0x25, 1, 1)
        address = Binary(address, 4, 4)
        binary = pre_prefix + prefix + reg + suffix + address 
        return binary, text

    @staticmethod
    def compare_register_one_with_register_two(reg1: int, reg2: int):
        text = binary_instruction_rr("CMP", reg1, reg2, 32)
        opcode = Binary(0x39, 1, 1)
        upper_64_prefix = Int32._calculate_prefix(reg1=reg1, reg2=reg2)
        register_pair = modrm(3, reg1, reg2)
        register_pair = Binary(register_pair, 1, 1)
        binary = upper_64_prefix + opcode + register_pair
        return binary, text
    
    @staticmethod
    def jump_if_equals(address: int):
        text = unary_instruction_imm("JE", address, 32)
        opcode = Binary(0x0F, 1, 1)
        opcode += Binary(0x84, 1, 1)
        address = Binary(address, 4, 4)
        binary = opcode + address
        return binary, text
    
    @staticmethod
    def jump_relative_near(const: int):
        """Relative to RIP, So 32 bit offset from RIP"""
        text = unary_instruction_imm("JMP", const, 32)
        opcode = Binary(0xE9, 1, 1)
        const = Binary(const, 4, 4)
        binary = opcode + const
        return binary, text

    @staticmethod
    def jump_absolute_near_indirect_m(address: int):
        """Relative to RIP, So 32 bit offset from RIP"""
        text = unary_instruction_m("JMP", address, 32)
        opcode = Binary(0xFF, 1, 1)
        opcode += Binary(0x24, 1, 1)
        opcode += Binary(0x25, 1, 1)
        address = Binary(address, 4, 4)
        binary = opcode + address
        return binary, text



if __name__ == "__main__":
    from utils import *
    # for i in range(0,16):
    #     for j in range(0,16):
    #         s = Int32.div_register_one_with_register_two(i)
    #         print(s[0])
    for i in range(0,16):
        s = Int32.idiv_register_one_with_register_two(i)
        print(s[0])
else:
    from tir.x86_64.utils import *
