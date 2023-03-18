from tir.parser.parser import Rules
from elfgenerator.Binary import Binary
from collections import deque
import tir.x86_64.x86_64 as asm
class InstructionSegment():


    def __init__(self, entry_point):
        self.instr_stack = deque()
        self.comment_stack = deque()
        self.permissions = 5
        self.start_position = 0
        self.end_position = 0
        self.set_entry_point(entry_point)

    def push_instr(self, binary_and_text: tuple[Binary, str]):
        instr = binary_and_text[0]
        comment = binary_and_text[1]
        self.end_position += instr.size
        self.instr_stack.append(instr)
        self.comment_stack.append(comment)

    def set_entry_point(self, entry_point):
        self.start_position += entry_point
        self.end_position += entry_point

    def __repr__(self):
        response = ""
        padding = 40
        total_instr = Binary(0,0,0)
        for index, i in enumerate(self.instr_stack):
            instr = i.__repr__()
            total_instr += i
            comment = self.comment_stack[index]
            response += instr + (padding-len(instr))*" " + "; "+ comment + "\n"
        response += "\n" + "Whole Binary: " + total_instr.__repr__() + "\n"
        return response
    
    def get_binary(self):
        bin = Binary(0,0,0)
        for i in self.instr_stack:
            bin += i
        return bin

    def get_assembly(self):
        asm = ""
        for i in self.comment_stack:
            asm += i + "\n"
        return asm

class Compiler():

    def __init__(self, symbol_table, TEXT_node):
        self.symbol_table = symbol_table
        entry_point = self.symbol_table.entry_point
        self.TEXT = InstructionSegment(entry_point)
        self.start_compiler(TEXT_node)

    def __repr__(self):
        string = "############# COMPILER START ########### \n"
        string += self.TEXT.__repr__()
        return string

    def start_compiler(self, TEXT_node):
        for child in TEXT_node.children:
            self.text_statement(child)
            
    def text_statement(self, text_statement_node):
        print(text_statement_node.type)
        if(text_statement_node.children[0].type == Rules.if_else_block):
            return


        variable_name = text_statement_node.children[0].content
        action_node = text_statement_node.children[1]
        if(action_node.type == Rules.add):
            self.add(variable_name, action_node)
            return
        elif(action_node.type == Rules.function_call):
            self.function_call(variable_name, action_node)
            return
        elif(action_node.type == Rules.subtract):
            self.subtract(variable_name, action_node)
            return
        elif(action_node.type == Rules.multiplication):
            self.imultiply(variable_name, action_node)
            return
        elif(action_node.type == Rules.division):
            self.udiv(variable_name, action_node)
            return
        elif(action_node.type == Rules.int):
            self.assign_int(variable_name, action_node)
            return
        else:
            raise Exception(f"Node of type {text_statement_node.children[1].type.name} has not been implemented yet.")


    def load_symbol(self, target_register, symbol_name):
        permissions, symbol_entry = self.symbol_table.get_symbol(symbol_name)
        registers = {"EAX": 0, "EDI": 7, "ECX": 1}
        target_register = registers[target_register]
        self.TEXT.push_instr(asm.Int32.load_memory_value_to_register_displacement_only(target_register, symbol_entry.address))
    
    def load_to_symbol(self, source_register, symbol_name):
        permissions, symbol_entry = self.symbol_table.get_symbol(symbol_name)
        registers = {"EAX": 0, "EDI": 7, "ECX": 1}
        source_register = registers[source_register]
        self.TEXT.push_instr(asm.Int32.load_register_value_to_memory_address_displacement_only(source_register, symbol_entry.address))

    def assign_int(self, destination, assign_node):
        self.TEXT.push_instr(asm.Int32.load_const_to_register_displacement_only(0, int(assign_node.content)))
        self.load_to_symbol("EAX", destination)

    def add(self, destination, add_node):
        LHS = add_node.children[0]
        RHS = add_node.children[1]
        if(LHS.type == Rules.variable and RHS.type == Rules.variable):
            p1, s1 = self.symbol_table.get_symbol(LHS.content)
            p2, s2 = self.symbol_table.get_symbol(RHS.content)
            if(s1.type == Rules.int_identifier and s2.type == Rules.int_identifier):
                self.load_symbol("EAX", LHS.content)
                self.load_symbol("EDI", RHS.content)
                self.TEXT.push_instr(asm.Int32.add_register_one_with_register_two(0, 7))
                self.load_to_symbol("EAX", destination)
                return
            else:
                raise NotImplementedError
        if(LHS.type == Rules.int and RHS.type == Rules.int):
            # Since both int immediates can be summed at compile time
            const = int(LHS.content) + int(RHS.content)
            self.TEXT.push_instr(asm.Int32.load_const_to_register_displacement_only(0, const))
            self.load_to_symbol("EAX", destination)
            return
        if(LHS.type == Rules.int and RHS.type == Rules.variable):
            self.TEXT.push_instr(asm.Int32.load_const_to_register_displacement_only(0, int(LHS.content)))
            self.load_symbol("EDI", RHS.content)
            self.TEXT.push_instr(asm.Int32.add_register_one_with_register_two(0, 7))
            self.load_to_symbol("EAX", destination)
            return
        if(LHS.type == Rules.variable and RHS.type == Rules.int):
            self.TEXT.push_instr(asm.Int32.load_const_to_register_displacement_only(0, int(RHS.content)))
            self.load_symbol("EDI", LHS.content)
            self.TEXT.push_instr(asm.Int32.add_register_one_with_register_two(0, 7))
            self.load_to_symbol("EAX", destination)
            return
        else:
            raise NotImplementedError
        
    def subtract(self, destination, sub_node):
        LHS = sub_node.children[0]
        RHS = sub_node.children[1]
        if(LHS.type == Rules.variable and RHS.type == Rules.variable):
            p1, s1 = self.symbol_table.get_symbol(LHS.content)
            p2, s2 = self.symbol_table.get_symbol(RHS.content)
            if(s1.type == Rules.int_identifier and s2.type == Rules.int_identifier):
                self.load_symbol("EAX", LHS.content)
                self.load_symbol("EDI", RHS.content)
                self.TEXT.push_instr(asm.Int32.subtract_register_one_with_register_two(0, 7))
                self.load_to_symbol("EAX", destination)
                return
            else:
                raise NotImplementedError
        if(LHS.type == Rules.int and RHS.type == Rules.int):
            # Since both int immediates can be summed at compile time
            const = int(LHS.content) - int(RHS.content)
            self.TEXT.push_instr(asm.Int32.load_const_to_register_displacement_only(0, const))
            self.load_to_symbol("EAX", destination)
            return
        if(LHS.type == Rules.int and RHS.type == Rules.variable):
            self.TEXT.push_instr(asm.Int32.load_const_to_register_displacement_only(0, int(LHS.content)))
            self.load_symbol("EDI", RHS.content)
            self.TEXT.push_instr(asm.Int32.subtract_register_one_with_register_two(0, 1))
            self.load_to_symbol("EAX", destination)
            return
        if(RHS.type == Rules.int and LHS.type == Rules.variable):
            self.TEXT.push_instr(asm.Int32.load_const_to_register_displacement_only(0, int(RHS.content)))
            self.load_symbol("EDI", LHS.content)
            self.TEXT.push_instr(asm.Int32.subtract_register_one_with_register_two(0, 1))
            self.load_to_symbol("EAX", destination)
            return
        else:
            raise NotImplementedError

    def imultiply(self, destination, imul_node):
        LHS = imul_node.children[0]
        RHS = imul_node.children[1]
        if(LHS.type == Rules.variable and RHS.type == Rules.variable):
            p1, s1 = self.symbol_table.get_symbol(LHS.content)
            p2, s2 = self.symbol_table.get_symbol(RHS.content)
            if(s1.type == Rules.int_identifier and s2.type == Rules.int_identifier):
                self.load_symbol("EAX", LHS.content)
                self.load_symbol("EDI", RHS.content)
                self.TEXT.push_instr(asm.Int32.signed_multiply_register_one_with_register_two(0,7))
                self.load_to_symbol("EAX", destination)
                return
            else:
                raise NotImplementedError
        if(LHS.type == Rules.int and RHS.type == Rules.int):
            # Since both int immediates can be summed at compile time
            const = int(LHS.content)*int(RHS.content)
            print("CONST IS ", const)
            self.TEXT.push_instr(asm.Int32.load_const_to_register_displacement_only(0, const))
            self.load_to_symbol("EAX", destination)
            return
        if(LHS.type == Rules.int and RHS.type == Rules.variable):
            self.TEXT.push_instr(asm.Int32.load_const_to_register_displacement_only(0, int(LHS.content)))
            self.load_symbol("EDI", RHS.content)
            self.TEXT.push_instr(asm.Int32.signed_multiply_register_one_with_register_two(0, 1))
            self.load_to_symbol("EAX", destination)
            return
        if(RHS.type == Rules.int and LHS.type == Rules.variable):
            self.TEXT.push_instr(asm.Int32.load_const_to_register_displacement_only(0, int(RHS.content)))
            self.load_symbol("EDI", LHS.content)
            self.TEXT.push_instr(asm.Int32.signed_multiply_register_one_with_register_two(0, 1))
            self.load_to_symbol("EAX", destination)
            return
        else:
            raise NotImplementedError
    
    def udiv(self, destination, div_node):
        LHS = div_node.children[0]
        RHS = div_node.children[1]
        if(LHS.type == Rules.variable and RHS.type == Rules.variable):
            p1, s1 = self.symbol_table.get_symbol(LHS.content)
            p2, s2 = self.symbol_table.get_symbol(RHS.content)
            if(s1.type == Rules.int_identifier and s2.type == Rules.int_identifier):
                self.load_symbol("EAX", LHS.content)
                self.load_symbol("EDI", RHS.content)
                self.TEXT.push_instr(asm.Int32.udiv_register_one_with_register_two(7))
                self.load_to_symbol("EAX", destination)
                return
            else:
                raise NotImplementedError
        if(LHS.type == Rules.int and RHS.type == Rules.int):
            # Since both int immediates can be summed at compile time
            const = int(LHS.content)//int(RHS.content)
            print("CONST IS ", const)
            self.TEXT.push_instr(asm.Int32.load_const_to_register_displacement_only(0, const))
            self.load_to_symbol("EAX", destination)
            return
        if(LHS.type == Rules.int and RHS.type == Rules.variable):
            self.TEXT.push_instr(asm.Int32.load_const_to_register_displacement_only(0, int(LHS.content)))
            self.load_symbol("EDI", RHS.content)
            self.TEXT.push_instr(asm.Int32.udiv_register_one_with_register_two(7))
            self.load_to_symbol("EAX", destination)
            return
        if(RHS.type == Rules.int and LHS.type == Rules.variable):
            self.TEXT.push_instr(asm.Int32.load_const_to_register_displacement_onlyy(7, int(RHS.content)))
            self.load_symbol("EAX", LHS.content)
            self.TEXT.push_instr(asm.Int32.udiv_register_one_with_register_two(7))
            self.load_to_symbol("EAX", destination)
            return
        else:
            raise NotImplementedError

    def function_call(self, destination, func_call_node):
        func_call_name = func_call_node.children[0].content
        syscall_regs = ["EAX", "EDI"]
        syscall_regs_as_int = [0,7]
        arguments = func_call_node.children
        for index, argument in enumerate(arguments):
            if(index == 0):
                continue
            if(argument.type == Rules.int):
                self.TEXT.push_instr(asm.Int32.load_const_to_register_displacement_only(syscall_regs_as_int[index-1], int(argument.content)))
            elif(argument.type == Rules.variable):
                self.load_symbol(syscall_regs[index-1], argument.content)
            else:
                raise NotImplementedError
        self.TEXT.push_instr(asm.syscall())


