import pytest

class Test_RODATA():

    # Rodata shares statements with data
    

    @pytest.mark.parametrize("src, answer, position", 
    [
    ('RODATA  \nx = int_32 is 64\ny=float_128[2000] is 90\n', True, 50), 
    ]) 
    def test_RODATA(self, parser, src, answer, position): # Note parser is provided by module fixture in conftest.py
        resultant_position, bool, node = parser.parse(src, parser.RODATA)
        if(node != None):
            node.pretty_print()
        assert bool == answer
        assert resultant_position == position