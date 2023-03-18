import pytest

test_1 = "TEXT\n"
test_1 += "if x > 25 { \n"
test_1 += "x = 100\n"
test_1 += "y = 200\n"
test_1 += "}\n"
test_1 = (test_1, True, len(test_1))

class Test_TEXT():

    @pytest.mark.parametrize("src, answer, position", 
    [
    ('x = 9 + 12\n', True, 11), 
    ('x=9 + 12\n', True, 9), 
    ('x = y/z\n', True, 8), 
    ('x = y-5    \n', True, 12), 
    ('x   = float_128[2000]  is 0\n', False, 0), 
    ('x =float_128 [2000] is \n', False, 0), # Only one space allowed between 
    ('x = 100\n', True, 8), 
    ('y=x()\n', True, 6), 
    ("y =x(25)\n", True, 9), 
    ("y = x(25, 190)\n", True, 15), 
    ("y =  x(25, y, z)\n", True, 17),
    ("y=hello()\n", True, 10),
    ("y= hello(25)\n", True, 13),
    ("y =hello(25, y)\n", True, 16),
    ("y = hello(25, y)\n", True, 17),
    ]) 
    def test_TEXT_statement(self, parser, src, answer, position): # Note parser is provided by module fixture in conftest.py
        resultant_position, bool, node = parser.parse(src, parser.TEXT_statement)
        if(node != None):
            node.pretty_print()
        assert bool == answer
        assert resultant_position == position
    

    @pytest.mark.parametrize("src, answer, position", 
    [
    ('TEXT  \nx = 5+9\n', True, 15), 
    ('TEXT  \nx = 5-9\n', True, 15), 
    ('TEXT  \nx = 5*9\n', True, 15), 
    ('TEXT  \nx = 5/9\n', True, 15), 
    ('TEXT  \nx = y+9\n', True, 15), 
    ('TEXT  \nx = y-9\n', True, 15), 
    ('TEXT  \nx = y*9\n', True, 15), 
    ('TEXT  \nx = y/9\n', True, 15), 
    ('TEXT  \nx = 5+z\n', True, 15), 
    ('TEXT  \nx = 5-z\n', True, 15), 
    ('TEXT  \nx = 5*z\n', True, 15), 
    ('TEXT  \nx = 5/z\n', True, 15), 
    ('TEXT      \nx = 5+9\ny=x-7\n', True, 25), 
    ('TEXT  \nx = hello()\n', True, 19), 
    ('TEXT  \nx = hello(26)\n', True, 21), 
    ('TEXT  \nx = hello(y, 50)\n', True, 24), 
    test_1,
    ]) 
    def test_TEXT(self, parser, src, answer, position): # Note parser is provided by module fixture in conftest.py
        resultant_position, bool, node = parser.parse(src, parser.TEXT)
        if(node != None):
            node.pretty_print()
        assert bool == answer
        assert resultant_position == position