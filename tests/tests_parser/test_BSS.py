import pytest

class Test_BSS():

    @pytest.mark.parametrize("src, answer, position", 
    [
    ('x = int_12\n', True, 11), 
    ('x = float_128[2000]\n', True, 20), 
    ('x = float_128[2000]    \n', True, 24), 
    ('x   = float_128[2000]\n', True, 22), 
    ('x =float_128 [2000]    \n', False, 0), # Only one space allowed between 
    ]) 
    def test_BSS_statement(self, parser, src, answer, position): # Note parser is provided by module fixture in conftest.py
        resultant_position, bool, node = parser.parse(src, parser.BSS_statement)
        if(node != None):
            node.pretty_print()
        assert bool == answer
        assert resultant_position == position
    

    @pytest.mark.parametrize("src, answer, position", 
    [
    ('BSS  \nx = int_32\ny=float_128[2000]\n', True, 35), 
    ]) 
    def test_BSS(self, parser, src, answer, position): # Note parser is provided by module fixture in conftest.py
        resultant_position, bool, node = parser.parse(src, parser.BSS)
        if(node != None):
            node.pretty_print()
        assert bool == answer
        assert resultant_position == position