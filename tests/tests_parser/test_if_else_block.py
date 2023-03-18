import pytest



test_1 = "if x > 25 { \n"
test_1 += "x = 100\n"
test_1 += "y = 200\n"
test_1 += "}\n"
test_1 = (test_1, True, len(test_1))

test_2 = "if x > 25 {\n"
test_2 += "x = 100\n"
test_2 += "y = 200\n"
test_2 += "}\n"
test_2 += "else {\n"
test_2 += "x = 100\n"
test_2 += "y = 200\n"
test_2 += "}\n"
test_2 = (test_2, True, len(test_2))


test_3 = "if x > 25 {\n"
test_3 += "x = 100 + n\n"
test_3 += "y = 200\n"
test_3 += "}\n"
test_3 += "else {\n"
test_3 += "x = y + z\n"
test_3 += "y = 200\n"
test_3 += "}\n"
test_3 = (test_3, True, len(test_3))



class Test_if_else_block():

    @pytest.mark.parametrize("src, answer, position", 
    [
    test_1,
    test_2,
    test_3,
    ]) 
    def test_if_else_block(self, parser, src, answer, position): # Note parser is provided by module fixture in conftest.py
        print(src, "\n", answer, "\n", position)
        resultant_position, bool, node = parser.parse(src, parser.if_else_block)
        print(resultant_position)
        if(node != None):
            node.pretty_print()
        assert bool == answer
        assert resultant_position == position
