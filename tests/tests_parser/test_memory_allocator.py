import pytest

class Test_memory_allocator():

    @pytest.mark.parametrize("src, answer, position", 
    [
    ('int_32[10]', True, 10), 
    ("int_32[0]", True, 9), 
    ("int_64", True, 6), 
    ("float_64[0]", True, 11),
    ("float_64[3]", True, 11),
    ("float_64[10]", True, 12),
    ]) 
    def test_memory_allocator(self, parser, src, answer, position): # Note parser is provided by module fixture in conftest.py
        resultant_position, bool, node = parser.parse(src, parser.memory_allocator)
        if(node != None):
            node.pretty_print()
        assert bool == answer
        assert resultant_position == position