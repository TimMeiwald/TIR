import pytest

class Test_if():

    @pytest.mark.parametrize("src, answer, position", 
    [
    ('if x > 25', True, 9), 
    ('if x > 25 ', True, 9), 
    ("if y <= x", True, 9), 
    ("if z<c", True, 6), 
    ("if 25<19", True, 8),
    ("if x==z", True, 7),
    ("if25<9", False, 0),
    ]) 
    def test_if(self, parser, src, answer, position): # Note parser is provided by module fixture in conftest.py
        resultant_position, bool, node = parser.parse(src, parser.if_statement)
        if(node != None):
            node.pretty_print()
        assert bool == answer
        assert resultant_position == position