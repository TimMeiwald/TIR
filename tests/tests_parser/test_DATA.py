import pytest

class Test_DATA():

    @pytest.mark.parametrize("src, answer, position", 
    [
    ('x = int_12 is 54\n', True, 17), 
    ('x = float_128[2000] is 201010\n', True, 30), 
    ('x = float_128[2000] is 0    \n', True, 29), 
    ('x   = float_128[2000]  is 0\n', True, 28), 
    ('x =float_128 [2000] is \n', False, 0), # Only one space allowed between 
    ]) 
    def test_BSS_statement(self, parser, src, answer, position): # Note parser is provided by module fixture in conftest.py
        resultant_position, bool, node = parser.parse(src, parser.DATA_statement)
        if(node != None):
            node.pretty_print()
        assert bool == answer
        assert resultant_position == position
    

    @pytest.mark.parametrize("src, answer, position", 
    [
    ('DATA  \nx = int_32 is 64\ny=float_128[2000] is 90\n', True, 48), 
    ]) 
    def test_BSS(self, parser, src, answer, position): # Note parser is provided by module fixture in conftest.py
        resultant_position, bool, node = parser.parse(src, parser.DATA)
        if(node != None):
            node.pretty_print()
        assert bool == answer
        assert resultant_position == position