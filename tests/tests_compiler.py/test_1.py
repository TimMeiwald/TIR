from tir.parser.parser import Grammar_Parser
from tir.compiler.symbolizer import SymbolTable
from tir.compiler.compiler import Compiler
def test_basic_compiler_operation():
    src = ""
    src += "DATA\n"
    src += "x = int_32 is 30\n"
    src += "RODATA\n"
    src += "y1 = int_32 is 22\n"
    src += "y2 = int_32[100] is 20\n"
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
    compiler = Compiler(sym_table, text_node)
    print(compiler)
    print(compiler.TEXT.get_assembly())
    print(compiler.TEXT.get_binary())
    # Running it primarily to check no exceptions thrown
    assert 0 == 1