import pytest

class Test_function_call():

    @pytest.mark.parametrize("src, answer, position", 
    [
    ('x()', True, 3), 
    ("x(25)", True, 5), 
    ("x(25, 190)", True, 10), 
    ("x(25, y, z)", True, 11),
    ("hello()", True, 7),
    ("hello(25)", True, 9),
    ("hello(25, y)", True, 12)
    ]) 
    def test_memory_allocator(self, parser, src, answer, position): # Note parser is provided by module fixture in conftest.py
        resultant_position, bool, node = parser.parse(src, parser.function_call)
        if(node != None):
            node.pretty_print()
        assert bool == answer
        assert resultant_position == position