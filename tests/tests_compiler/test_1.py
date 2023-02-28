from tir.parser.parser import Grammar_Parser
from tir.compiler.symbolizer import SymbolTable
from tir.compiler.compiler import Compiler
from tir.compiler.assembler import Assembler, Architecture
import os as os
import subprocess

def writeout_executable(func):
    """Provided a test returns the Binary executable then it'll be written out 
    to a file in the test output folder named after the test name"""
    name = func.__name__
    def kernel(*args, **kwargs):
        exe = func(*args, **kwargs)
        path = os.path.join(os.getcwd(), "tests", "tests_compiler", "test_output", f"{name}.elf")
        with open(path, "wb+") as fp:
            fp.write(exe.binary())
        return 
    return kernel()


@writeout_executable
def test_very_basic_compiler_operation():
    src = ""
    src += "TEXT\n"
    src += "z = syscall(60, 45)\n"
    src += "\n"
    parser = Grammar_Parser()
    resultant_position, bool, node = parser.parse(src, parser.grammar)
    sym_table = SymbolTable()
    text_node = sym_table.symbolize(node)
    print(sym_table)
    compiler = Compiler(sym_table, text_node)
    print(compiler)
    exe = Assembler(sym_table.DATA, sym_table.RODATA, sym_table.BSS, compiler.TEXT, arch=Architecture.x86_64).get_executable()
    print("\n\n######## Executable #########")
    print(exe)
    return exe

@writeout_executable
def test_very_basic_compiler_operation2():
    src = ""
    src += "DATA\n"
    src += "x = int_32 is 60\n"
    src += "y = int_32 is 47\n"
    src += "TEXT\n"
    src += "z = syscall(x, y)\n"
    src += "\n"
    parser = Grammar_Parser()
    resultant_position, bool, node = parser.parse(src, parser.grammar)
    if(node == None):
        raise Exception("Failed to Parse", resultant_position, bool)
    sym_table = SymbolTable()
    text_node = sym_table.symbolize(node)
    print(sym_table)
    compiler = Compiler(sym_table, text_node)
    print(compiler)
    exe = Assembler(sym_table.DATA, sym_table.RODATA, sym_table.BSS, compiler.TEXT, arch=Architecture.x86_64).get_executable()
    return exe

@writeout_executable
def test_basic_compiler_operation():
    src = ""
    src += "DATA\n"
    src += "x = int_32 is 30\n"
    src += "RODATA\n"
    src += "y1 = int_32 is 22\n"
    src += "y2 = int_32[4] is 20\n"
    src += "y3 = int_32 is 10\n"
    src += "BSS\n"
    src += "z = int_32\n"
    src += "TEXT\n"
    src += "z = y1 + y2\n"
    src += "x = 40 + 20\n"
    src += "z = syscall(x, z)\n"
    src += "\n"
    parser = Grammar_Parser()
    resultant_position, bool, node = parser.parse(src, parser.grammar)
    sym_table = SymbolTable()
    text_node = sym_table.symbolize(node)
    print(sym_table)
    compiler = Compiler(sym_table, text_node)
    print(compiler)
    exe = Assembler(sym_table.DATA, sym_table.RODATA, sym_table.BSS, compiler.TEXT, arch=Architecture.x86_64).get_executable()
    return exe

@writeout_executable
def test_basic_add():
    src = ""
    src += "DATA\n"
    src += "x = int_32 is 30\n"
    src += "RODATA\n"
    src += "y1 = int_32 is 22\n"
    src += "y2 = int_32[4] is 20\n"
    src += "y3 = int_32 is 10\n"
    src += "BSS\n"
    src += "z = int_32\n"
    src += "TEXT\n"
    src += "z = y1 + y2\n"
    src += "x = 40 + 20\n"
    src += "z = syscall(x, z)\n"
    src += "\n"
    parser = Grammar_Parser()
    resultant_position, bool, node = parser.parse(src, parser.grammar)
    sym_table = SymbolTable()
    text_node = sym_table.symbolize(node)
    print(sym_table)
    compiler = Compiler(sym_table, text_node)
    print(compiler)
    exe = Assembler(sym_table.DATA, sym_table.RODATA, sym_table.BSS, compiler.TEXT, arch=Architecture.x86_64).get_executable()
    return exe

@writeout_executable
def test_basic_sub():
    src = ""
    src += "DATA\n"
    src += "x = int_32 is 30\n"
    src += "RODATA\n"
    src += "y1 = int_32 is 22\n"
    src += "y2 = int_32[4] is 20\n"
    src += "y3 = int_32 is 10\n"
    src += "BSS\n"
    src += "z = int_32\n"
    src += "TEXT\n"
    src += "z = y1 - y2\n"
    src += "x = 40 + 20\n"
    src += "z = syscall(x, z)\n"
    src += "\n"
    parser = Grammar_Parser()
    resultant_position, bool, node = parser.parse(src, parser.grammar)
    sym_table = SymbolTable()
    text_node = sym_table.symbolize(node)
    print(sym_table)
    compiler = Compiler(sym_table, text_node)
    print(compiler)
    exe = Assembler(sym_table.DATA, sym_table.RODATA, sym_table.BSS, compiler.TEXT, arch=Architecture.x86_64).get_executable()
    return exe