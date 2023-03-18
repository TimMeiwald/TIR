from tir.parser.parser import Grammar_Parser
from tir.compiler.symbolizer import SymbolTable
from tir.compiler.compiler import Compiler
from tir.compiler.assembler import Assembler, Architecture
import os as os
import subprocess
from functools import wraps


def writeout_executable(func):
    """Provided a test returns the Binary executable then it'll be written out 
    to a file in the test output folder named after the test name."""
    name = func.__name__
    current_file_name = __file__
    if(os.name == "nt"):
        current_file_name = current_file_name.split("\\")[-1]
    elif(os.name == "posix"):
        current_file_name = current_file_name.split("/")[-1]
    else:
        raise Exception("Unknown Operating System")
    @wraps(func)
    def kernel(*args, **kwargs):
        exe, ret_code = func(*args, **kwargs)
        path = str(f"{current_file_name[:-3]}_{name}.elf")
        path = os.path.join(os.getcwd(), "tests", "tests_compiler", "test_output", path)
        with open(path, "wb+") as fp:
            fp.write(exe.binary())
        return exe, ret_code
    return kernel

def run_wsl_code(func):
    """Runs the executable and gets the return code"""
    name = func.__name__
    current_file_name = __file__
    if(os.name == "nt"):
        current_file_name = current_file_name.split("\\")[-1]
    elif(os.name == "posix"):
        current_file_name = current_file_name.split("/")[-1]
    else:
        raise Exception("Unknown Operating System")
    @wraps(func)
    def kernel(*args, **kwargs):
        if(os.name == "nt"):
            pwd = subprocess.check_output(['wsl', 'pwd'])
            pwd = str(pwd,encoding="utf-8").replace("\n", "")
        else:
            pwd = os.getcwd()
        pwd += "/tests/tests_compiler/test_output/" + current_file_name[:-3] + "_" + name + ".elf" # Intentionally not platform agnostic so it can run on wsl too.
        exe, ret_code = func(*args, **kwargs)
        try:
            executable_return_code = subprocess.check_call(['wsl', pwd])
        except subprocess.CalledProcessError as e:
            executable_return_code = e.returncode
            # Want to ignore this exception because it raises an error on a return code of anything non-zero
            # But we want to intentionally do that so we can test if the compiler works.
            pass
        assert executable_return_code == ret_code
        return None
    return kernel


@run_wsl_code
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
    return exe, 45

@run_wsl_code
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
    return exe, 47

@run_wsl_code
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
    return exe, 42

@run_wsl_code
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
    return exe, 42

@run_wsl_code
@writeout_executable
def test_basic_add_one_side_var():
    src = ""
    src += "DATA\n"
    src += "x = int_32 is 40\n"
    src += "RODATA\n"
    src += "y1 = int_32 is 22\n"
    src += "y2 = int_32 is 20\n"
    src += "BSS\n"
    src += "z = int_32\n"
    src += "TEXT\n"
    src += "z = 22 + y2\n"
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
    return exe, 42

@run_wsl_code
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
    return exe, 2


@run_wsl_code
@writeout_executable
def test_basic_signed_mul():
    src = ""
    src += "DATA\n"
    src += "x = int_32 is 30\n"
    src += "RODATA\n"
    src += "y1 = int_32 is 22\n"
    src += "y2 = int_32[4] is 20\n"
    src += "y3 = int_32 is 10\n"
    src += "y4 = int_32 is 4\n"
    src += "y5 = int_32 is 6\n"
    src += "BSS\n"
    src += "z = int_32\n"
    src += "TEXT\n"
    src += "z = y4 * y5\n"
    src += "x = 40+20\n"
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
    return exe, 24

@run_wsl_code
@writeout_executable
def test_basic_unsigned_div():
    src = ""
    src += "DATA\n"
    src += "x = int_32 is 40\n"
    src += "RODATA\n"
    src += "y4 = int_32 is 30\n"
    src += "y5 = int_32 is 2\n"
    src += "BSS\n"
    src += "z = int_32\n"
    src += "TEXT\n"
    src += "z = y4 / y5\n"
    src += "x = x+20\n"
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
    return exe, 15


@run_wsl_code
@writeout_executable
def test_basic_unsigned_div():
    src = ""
    src += "DATA\n"
    src += "x = int_32 is 40\n"
    src += "RODATA\n"
    src += "y4 = int_32 is 30\n"
    src += "y5 = int_32 is 2\n"
    src += "BSS\n"
    src += "z = int_32\n"
    src += "TEXT\n"
    src += "z = 100 / y5\n"
    src += "x = x+20\n"
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
    return exe, 50



@run_wsl_code
@writeout_executable
def test_basic_if_else_block():
    src = ""
    src += "DATA\n"
    src += "x = int_32 is 40\n"
    src += "RODATA\n"
    src += "y = int_32 is 30\n"
    src += "BSS\n"
    src += "z = int_32\n"
    src += "TEXT\n"
    src += "z = 100\n"
    src += "if x > 25 {\n"
    src += "y = 2400\n"
    src += "x = y/x\n"
    src += "}\n"
    src += "else {\n"
    src += "z = 400\n"
    src += "}\n"
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
    return exe, 50