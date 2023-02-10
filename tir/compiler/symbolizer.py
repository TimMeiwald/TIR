from tir.parser.parser import Rules
from enum import IntEnum
from tir.compiler.compiler import Compiler
class SymbolTableEntry():

    def __init__(self, name: str, typ: IntEnum, size: int, quantity: int, value=None):
        self.name = name
        self.type = typ
        self.size = size
        self.quantity = quantity
        self.value = value
        self.address = None
    
    def __repr__(self):
        return f"(Name: {self.name}, Type: {self.type.name}, Bytes per Type: {self.size}, Number of Type: {self.quantity}, Total Bytes Required: {self.size*self.quantity}, Address: {self.address} with value: {self.value})"

class DataSegment():

    def __init__(self, permissions: int):
        self.symbols = []
        self.lookup = {}
        self.position = 0
        self.permissions = permissions
    
    def set_symbol(self, symbol_entry: SymbolTableEntry):
        symbol_entry.address = self.position
        self.position += symbol_entry.size*symbol_entry.quantity
        self.lookup[symbol_entry.name] = len(self.symbols)
        self.symbols.append(symbol_entry)

    def get_symbol(self, symbol_name: str):
        try:
            s = self.lookup[symbol_name]
            return self.symbols[s]
        except KeyError as e:
            raise KeyError(f"Could not find symbol: {symbol_name} \n{e}")
    
    def __repr__(self):
        string = ""
        for symbol in self.symbols:
            string += symbol.__repr__()
            string += "\n"
        return string 

    def shift_memory_addresses(self, shift_size: int):
        for entry in self.symbols:
            entry.address += shift_size
        

class SymbolTable():


    def __init__(self):
        self.BSS = DataSegment(6) # -RW -> Is for Data initialised at runtime
        self.DATA = DataSegment(6) # -RW -> For Data stored at compile time
        self.RODATA = DataSegment(4) # -R- 
        self.entry_point = None

    def get_symbol(self, symbol_name: str):
        try:
            return (self.BSS.permissions, self.BSS.get_symbol(symbol_name))
        except KeyError:
            pass
        try:
            return (self.DATA.permissions, self.DATA.get_symbol(symbol_name))
        except KeyError:
            pass
        try:
            return (self.RODATA.permissions, self.RODATA.get_symbol(symbol_name))
        except KeyError:
            pass
        # If here nothing
        raise KeyError(f"Could not find symbol with name {symbol_name}")
    
    def linearize_memory_addresses(self, page_size):
        data_segments = [self.DATA, self.RODATA, self.BSS]
        page_count = 0 # 0th page for program header entries and header. 64 Bytes + 56 Bytes per segment * 3 segments = 232 bytes
        for segment in data_segments:
            size_bytes = segment.position
            size_pages = ((size_bytes//page_size)+1)
            size_bytes = size_pages*page_size # 1 Page larger than integer div
            shift = size_bytes + page_count*page_size
            page_count += size_pages
            segment.shift_memory_addresses(shift)
        self.entry_point = (page_count+1)*page_size


    def symbolize(self, AST):
        """Runs through the AST and extracts all data segments, then returns the TEXT AST Node for further compiling."""
        print("#### AST ####")
        AST.pretty_print()
        print("\n\n\n")
        print("#### Symbol Table Start ####")
        text = None
        for child in AST.children:
            if(child.type == Rules.DATA):
                self.symbolize_DATA(child)
            elif(child.type == Rules.RODATA):
                self.symbolize_RODATA(child)
            elif(child.type == Rules.BSS):
                self.symbolize_BSS(child)
            elif(child.type == Rules.TEXT):
                text = child
                break
            else:
                raise NotImplementedError(f"Have not implemented node of type: {child.type} yet.")
        print(self)
        self.linearize_memory_addresses(4096)
        print(self)
        print("\n\n\n")
        return text

    def symbolize_DATA(self, data_node):
        for child in data_node.children:
            if(child.type != Rules.DATA_statement):
                raise Exception("symbolizer Error")
            y = self.data_statement(child)
            self.DATA.set_symbol(y)
    
    def symbolize_RODATA(self, data_node):
        for child in data_node.children:
            if(child.type != Rules.DATA_statement):
                raise Exception("symbolizer Error")
            y = self.data_statement(child)
            self.RODATA.set_symbol(y)
    
    def symbolize_BSS(self, data_node):
        for child in data_node.children:
            if(child.type != Rules.BSS_statement):
                raise Exception("symbolizer Error")
            y = self.BSS_statement(child)
            self.BSS.set_symbol(y)
        
    def BSS_statement(self, data_node):
        name = data_node.children[0].content
        memory_reqs = data_node.children[1]
        type, size, quantity = self.memory_allocator(memory_reqs)
        s = SymbolTableEntry(name, type, size, quantity)
        return s

    def data_statement(self, data_node):
        name = data_node.children[0].content
        memory_reqs = data_node.children[1]
        type, size, quantity = self.memory_allocator(memory_reqs)
        if(type==Rules.int_identifier):
            value = data_node.children[2].content
            value = int(value)
        else:
            raise TypeError("Have not yet implemented type {type} yet.")
        s = SymbolTableEntry(name, type, size, quantity, value)
        return s

    def memory_allocator(self, memory_alloc_node):
        type = memory_alloc_node.children[0].type
        size = int(memory_alloc_node.children[1].content)
        size = size//8 # To convert to bytes
        try:
            quantity = int(memory_alloc_node.children[2].content)
            if(quantity == 0):
                quantity = 1
        except IndexError:
            quantity = 1
        return type, size, quantity
    
    def __repr__(self):
        string = ""
        string += f"entry_point: {self.entry_point}\n"
        string +="DATA\n"
        string += self.DATA.__repr__()
        string +="\nRODATA\n"
        string += self.RODATA.__repr__()
        string +="\nBSS\n"
        string += self.BSS.__repr__()
        return string
    