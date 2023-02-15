from tir.compiler.symbolizer import DataSegment, SymbolTableEntry
from enum import IntEnum

class simulated_int_enum(IntEnum):
    x = 1

def test_basic_set_symbol():
    enum = simulated_int_enum.x
    s = SymbolTableEntry("Test", enum, 1, 1, 0)
    d = DataSegment(7)
    d.set_symbol(s)
    assert d.symbols[0] == s
    assert d.symbols[0].name == "Test"
    assert d.symbols[0].type.value == 1
    assert d.symbols[0].size == 1
    assert d.symbols[0].quantity == 1
    assert d.symbols[0].value == 0


def test_basic_get_symbol():
    enum = simulated_int_enum.x
    s = SymbolTableEntry("Test", enum, 1, 1, 0)
    d = DataSegment(7)
    d.set_symbol(s)
    x = d.get_symbol("Test")
    assert x == s
    assert x.name == "Test"
    assert x.type.value == 1
    assert x.size == 1
    assert x.quantity == 1
    assert x.value == 0

def test_basic_size_tracking():
    enum = simulated_int_enum.x
    s = SymbolTableEntry("Test", enum, 1, 1, 0) # 1 byte
    s2 = SymbolTableEntry("Test", enum, 4, 1, 0) # 4 bytes
    s3 = SymbolTableEntry("Test", enum, 2, 100, 0) # 200 bytes
    d = DataSegment(7)
    d.set_symbol(s)
    assert d.end_position == 1
    d.set_symbol(s2)
    assert d.end_position == 5
    d.set_symbol(s3)
    assert d.end_position == 205
