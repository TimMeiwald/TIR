from tir.parser.parser import Grammar_Parser
import pytest
from os import getcwd
from os.path import join
from pathlib import Path
import os

@pytest.fixture(autouse = True)
def parser():
    parser = Grammar_Parser()
    return parser




def compiler_test(test_num: int):
    with open(join(getcwd(), "tests", "test_compiler", f"Test{test_num}.txt"),"r") as fp:
        src = fp.read()
    p = Grammar_Parser()
    position, bool, node = p.parse(src, p.grammar)
    assert bool == True
    node.pretty_print()
    print("######################################################\n")
    assert position == len(src)
    return node