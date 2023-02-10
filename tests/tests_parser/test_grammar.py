import pytest

class Test_grammar():

   
    def test_basic_program_parsing(self, parser): # Note parser is provided by module fixture in conftest.py
        src = ""
        src += "DATA\n"
        src += "x = int_32 is 60\n"
        src += "RODATA\n"
        src += "y1 = int_32 is 22\n"
        src += "y2 = int_32 is 20\n"
        src += "BSS\n"
        src += "z = int_32\n"
        src += "TEXT\n"
        src += "z = y1 + y2\n"
        src += "\n"


        resultant_position, bool, node = parser.parse(src, parser.grammar)
        if(node != None):
            node.pretty_print()
        answer = True
        position = 98
        assert bool == answer
        assert resultant_position == position
    

    def test_basic_program_parsing2(self, parser): # Note parser is provided by module fixture in conftest.py
        src = ""
        src += "DATA\n"
        src += "x = int_32 is 60\n"
        src += "RODATA\n"
        src += "y1 = int_32 is 22\n"
        src += "y2 = int_32 is 20\n"
        src += "BSS\n"
        src += "z = int_32\n"
        src += "TEXT\n"
        src += "z = y1 + y2\n"
        src += "z = syscall(60, z)\n"


        resultant_position, bool, node = parser.parse(src, parser.grammar)
        if(node != None):
            node.pretty_print()
        answer = True
        position = 116
        assert bool == answer
        assert resultant_position == position

    

    def test_basic_program_parsing3(self, parser): # Note parser is provided by module fixture in conftest.py
        src = ""
        src += "DATA\n"
        src += "x = int_32[400] is 60\n"
        src += "RODATA\n"
        src += "y1 = int_32[28] is 22\n"
        src += "y2 = int_32[1] is 20\n"
        src += "BSS\n"
        src += "z = int_32[100]\n"
        src += "TEXT\n"
        src += "z = y1 + y2\n"
        src += "z = syscall(60, z)\n"


        resultant_position, bool, node = parser.parse(src, parser.grammar)
        if(node != None):
            node.pretty_print()
        answer = True
        position = 133
        assert bool == answer
        assert resultant_position == position
