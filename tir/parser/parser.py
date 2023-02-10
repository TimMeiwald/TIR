from collections import deque
from functools import lru_cache as cache
from enum import IntEnum


class Rules(IntEnum):
    _ROOT = 0
    _TERMINAL = 1
    _SEQUENCE = 2
    _ORDERED_CHOICE = 3
    _NOT_PREDICATE = 4
    _AND_PREDICATE = 5
    _OPTIONAL = 6
    _ZERO_OR_MORE = 7
    _ONE_OR_MORE = 8
    _SUBEXPRESSION = 10
    _VAR_NAME = 11
    _test = 12
    # Following enum values are all autogenerated from grammar file
    Alphabet_Upper = 20
    Alphabet_Lower = 21
    Num = 22
    Spaces = 23
    Specials = 24
    ASCII = 25
    newline = 26
    space = 27
    whitespace = 28
    equals = 29
    underscore = 30
    open_square_bracket = 31
    close_square_bracket = 32
    open_bracket = 33
    close_bracket = 34
    Is = 35
    comma = 36
    integer = 37
    variable = 38
    line_terminator = 39
    size = 40
    quantity = 41
    memory_allocator = 42
    int_identifier = 43
    float_identifier = 44
    type_identifier = 45
    plus = 46
    minus = 47
    forward_slash = 48
    star = 49
    add = 50
    subtract = 51
    division = 52
    multiplication = 53
    maths = 54
    function_call = 55
    int = 56
    data = 57
    BSS_statement = 58
    DATA_statement = 59
    TEXT_statement = 60
    RODATA_identifier = 61
    DATA_identifier = 62
    BSS_identifier = 63
    TEXT_identifier = 64
    RODATA = 65
    DATA = 66
    BSS = 67
    TEXT = 68
    grammar = 69



class Node():
    """Core data type"""

    def __init__(self, type: int, content: str = ""):
        """Constructor

        Args:
            type (int): int that corresponds to Rules IntEnum telling you what type of Node it is.
            content (str, optional): Content of Node. Defaults to "".
        """
        self.type = type
        self.content = content
        self.children = deque()
        self.parent = None

    def appender(self, node_deque):
        if (isinstance(node_deque, tuple)):
            print("Tuple apparently: ", node_deque)
            raise Exception
        if (node_deque is None):
            return None
        elif (not isinstance(node_deque, deque)):
            self.children.append(node_deque)
        else:
            for child in node_deque:
                self.appender(child)

    def __equals(self, __o: object) -> bool:
        if (__o is None):
            return False
        if (self.content == __o.content and self.type.name == __o.type.name):
            # By name of type as opposed to value because the value can change between
            # parser versions as the enum is autogenerated
            return True
        else:
            return False

    def __eq__(self, __o: object) -> bool:
        """Two Nodes are considered equal if they and all their subchildren have identical types and contents in order"""
        return self.__subtree_equals(__o)

    def __subtree_equals(self, __o: object) -> bool:
        if (self.__equals(__o) is False):
            return False
        else:
            count = 0
            for index, child in enumerate(self.children):
                try:
                    bool = child.__subtree_equals(__o.children[index])
                    count += bool
                except IndexError:
                    return False
            if (count != len(self.children)):
                return False
            else:
                return True

    def pretty_print(self):
        self._pretty_print(self)

    def _pretty_print(self, node, indent=0):
        indent_str = "  "
        if (node is not None):
            print(indent_str * indent +
                  f"Node: {node.type.name}, '{node.content}'")
            for child in node.children:
                self._pretty_print(child, indent + 1)


class Parser():

    def __init__(self):
        self.src = ""

    def _set_src(self, src: str):
        self.src = src
        # Ensures all caches are cleared on resetting the src
        # Resets state completely
        for rule in Rules:
            # Less than 20 is core parser stuff, greater than 20 is inherited
            # class stuff
            if (rule > 0 and rule < 20):
                func = getattr(self, rule.name)
                func.cache_clear()

    def caller(self, position, func, arg=None):
        """Calls generated functions, ensures converted to node not nested deques,
        Useful for testing or calling specific subterminals"""
        return self._VAR_NAME(position, (func, arg))

    def parse(self, src, func, *, arg=None):
        """Pass in the src and the function from the Grammar_Parser class you defined in the Grammar file
        and it will parse it and return the position at which halting stopped, whether the parse succeeded
        and the AST."""
        self._set_src(src)
        position, bool, node = self._VAR_NAME(0, (func, arg))
        if(node is not None):
            pass_two = Parser_Pass_Two()
            pass_two.parse(node)
            return position, bool, node
        else:
            return position, bool, None

    @cache
    def _token(self, position):
        if (position >= len(self.src)):
            return False
        return self.src[position]

    @cache
    def _TERMINAL(self, position: int, arg: str):
        #assert type(position) == int
        #assert type(Arg) == str
        if(arg == ""):
            node = Node(Rules._TERMINAL, None)
            return position, True, node
        token = self._token(position)
        if (token == arg):
            position += 1
            if (token == "\\"):
                token = self._token(position)
                if (token == "n"):
                    position += 1
                    token = "\\n"
                elif (token == "r"):
                    position += 1
                    token = "\\r"
                elif (token == "t"):
                    position += 1
                    token = "\\t"
                else:
                    token = "\\"
            node = Node(Rules._TERMINAL, token)
            return position, True, node
        else:
            # Don't generate anything other than terminal and var on run, means
            # no rationalizer
            return position, False, None

    @cache
    def _VAR_NAME(self, position: int, args):
        """True if called function evaluates to true else false, Is used to call other functions."""
        # where func is a grammar rule
        temp_position = position
        func, args = args
        position, bool, node = func(position, args)
        if (bool):
            key = func.__name__
            var_node = Node(Rules[key], None)
            if (node is not None):
                var_node.appender(node)
                return position, True, var_node
            else:
                return position, True, None
        else:
            position = temp_position
            return position, False, None

    @cache
    def _ORDERED_CHOICE(self, position: int, args):
        """True if one expression matches, then updates position, else false, no positional update"""
        LHS_func, LHS_arg = args[0]
        RHS_func, RHS_arg = args[1]
        temp_position = position
        position, bool, node = LHS_func(position, LHS_arg)
        if (bool):
            return position, True, node
        position = temp_position
        position, bool, node = RHS_func(position, RHS_arg)
        if (bool):
            return position, True, node
        position = temp_position
        return position, False, None

    @cache
    def _SEQUENCE(self, position: int, args):
        """True if all expressions match, then updates position, else false, no positional update"""
        temp_position = position
        LHS_func, LHS_arg = args[0]
        RHS_func, RHS_arg = args[1]
        position, bool, lnode = LHS_func(position, LHS_arg)
        if (bool):
            position, bool, rnode = RHS_func(position, RHS_arg)
            if (bool):
                node = deque()
                node.append(lnode)
                node.append(rnode)
                return position, True, node
            else:
                position = temp_position
                return position, False, None
        else:
            position = temp_position
            return position, False, None

    @cache
    def _ZERO_OR_MORE(self, position: int, args):
        """Always True, increments position each time the expression matches else continues without doing anything"""
        func, arg = args
        zero_nodes = deque()
        while (True):
            temp_position = position
            position, bool, term_node = func(temp_position, arg)
            if (bool):
                zero_nodes.append(term_node)
                continue
            else:
                position = temp_position
                break
        if (len(zero_nodes) == 0):
            return position, True, None
        else:
            return position, True, zero_nodes

    @cache
    def _ONE_OR_MORE(self, position: int, args):
        """Always True, increments position each time the expression matches else continues without doing anything"""
        func, arg = args
        one_nodes = deque()
        while (True):
            temp_position = position
            position, bool, term_node = func(temp_position, arg)
            if (bool):
                one_nodes.append(term_node)
                continue
            else:
                position = temp_position
                break
        if (len(one_nodes) == 0):
            return position, False, None
        else:
            return position, True, one_nodes

    @cache
    def _OPTIONAL(self, position: int, args):
        """Always True, increments position if option matches otherwise continues without doing anything"""
        func, arg = args
        temp_position = position
        position, bool, node = func(temp_position, arg)
        if (bool):
            return position, True, node
        else:
            position = temp_position
            return position, True, None

    @cache
    def _AND_PREDICATE(self, position: int, args):
        """True if the function results in True, never increments position"""
        func, arg = args
        temp_position = position
        position, bool, node = func(position, arg)
        if (bool):
            position = temp_position
            return position, True, None
        else:
            position = temp_position
            return position, False, None

    @cache
    def _NOT_PREDICATE(self, position: int, args):
        """True if the function results in False, never increments position"""
        position, bool, node = self._AND_PREDICATE(position, args)
        return position, not bool, None

    @cache
    def _SUBEXPRESSION(self, position: int, args):
        """Subexpression is any expression inside a pair of () brackets
        SUBEXPR essentially does nothing but allows for order of precedent
        more importantly order of precedence is very restricted because it made my life hard
        (mostly because I can't find a good definition of what order of precedence is in PEG) so use SUBEXPR
        to make more complicated rules"""
        func, arg = args
        temp_position = position
        position, bool, node = func(position, arg)
        if (bool):
            return position, True, node
        else:
            position = temp_position
            return position, False, None

    @cache
    def _test(self, position: int, args):
        """For testing purposes, may be able to refactor somehow to test
        but not sure how"""
        return self._TERMINAL(position, args)

class Parser_Pass_Two():

    def __init__(self):
        self.delete_nodes = (Rules.newline, Rules.space, Rules.whitespace, Rules.equals, Rules.underscore, Rules.open_square_bracket, Rules.close_square_bracket, Rules.open_bracket, Rules.close_bracket, Rules.Is, Rules.comma, Rules.line_terminator, Rules.plus, Rules.minus, Rules.forward_slash, Rules.star, Rules.RODATA_identifier, Rules.DATA_identifier, Rules.BSS_identifier, Rules.TEXT_identifier, )
        self.passthrough_nodes = (Rules.Alphabet_Upper, Rules.Alphabet_Lower, Rules.Num, Rules.Spaces, Rules.Specials, Rules.ASCII, Rules.integer, Rules.type_identifier, Rules.maths, Rules.data, )
        self.collect_nodes = (Rules.variable, Rules.size, Rules.quantity, Rules.int_identifier, Rules.float_identifier, Rules.int, )
        # Anyone making modifications be aware everything after line 10 is
        # automatically added to
        self.tokens = deque()
        # generated parsers while everything before it isn't(so I can add the
        # right stuff based on grammar)

    def token_generator(self, node):
        self.tokens.append(node)
        for child in node.children:
            child.parent = node
            self.token_generator(child)

    def delete_kernel(self, node):
        if (node.type in self.delete_nodes):
            node.children = deque()
            if(node.parent is not None):
                node.parent.children.remove(node)
            del node
        else:
            return node

    def passthrough_kernel(self, node):
        if (node.type in self.passthrough_nodes):
            if(node.parent is not None):
                index = node.parent.children.index(node)
                node.children.reverse()
                for child in node.children:
                    node.parent.children.insert(index, child)
                node.parent.children.remove(node)
            del node
        else:
            return node

    def collect_kernel(self, node):
        if (node.type in self.collect_nodes):
            for child in node.children:
                if (child.type != Rules._TERMINAL):
                    raise ValueError(
                        f"Cannot collect if there are non terminals in the nodes childrens. Node_Type: {node.type.name}, Child_Type: {child.type.name}")
            node.content = ""
            for child in node.children:
                node.content += child.content
            node.children = deque()
            return node
        else:
            return node

    def __parse(self, nodes):
        new_deq = deque()
        for index in range(0, len(nodes)):
            node = nodes.pop()
            node = self.delete_kernel(node)
            if (node is not None):
                node = self.passthrough_kernel(node)
            if (node is not None):
                node = self.collect_kernel(node)
            if (node is not None):
                new_deq.append(node)
        return new_deq

    def parse(self, node):
        self.token_generator(node)
        nodes = deque(self.tokens)
        nodes = self.__parse(nodes)
        return nodes



class Grammar_Parser(Parser):

    def _set_src(self, src: str):
        super()._set_src(src)
        for rule in Rules:
            if(rule >= 20): #Less than 20 is core parser stuff, greatereq than 20 is inherited class stuff
                func = getattr(self, rule.name)
                func.cache_clear()

    @cache
    def Alphabet_Upper(self, position: int, dummy = None):
        """
        <Alphabet_Upper> = "A"/"B"/"C"/"D"/"E"/"F"/"G"/"H"/"I"/"J"/"K"/"L"/"M"/"N"/"O"/"P"/"Q"/"R"/"S"/"T"/"U"/"V"/"W"/"X"/"Y"/"Z" ;
        """
        return self._SUBEXPRESSION(position, (self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._TERMINAL, "A"), (self._TERMINAL, "B"))), (self._TERMINAL, "C"))), (self._TERMINAL, "D"))), (self._TERMINAL, "E"))), (self._TERMINAL, "F"))), (self._TERMINAL, "G"))), (self._TERMINAL, "H"))), (self._TERMINAL, "I"))), (self._TERMINAL, "J"))), (self._TERMINAL, "K"))), (self._TERMINAL, "L"))), (self._TERMINAL, "M"))), (self._TERMINAL, "N"))), (self._TERMINAL, "O"))), (self._TERMINAL, "P"))), (self._TERMINAL, "Q"))), (self._TERMINAL, "R"))), (self._TERMINAL, "S"))), (self._TERMINAL, "T"))), (self._TERMINAL, "U"))), (self._TERMINAL, "V"))), (self._TERMINAL, "W"))), (self._TERMINAL, "X"))), (self._TERMINAL, "Y"))), (self._TERMINAL, "Z"))))

    @cache
    def Alphabet_Lower(self, position: int, dummy = None):
        """
        <Alphabet_Lower> = "a"/"b"/"c"/"d"/"e"/"f"/"g"/"h"/"i"/"j"/"k"/"l"/"m"/"n"/"o"/"p"/"q"/"r"/"s"/"t"/"u"/"v"/"w"/"x"/"y"/"z" ;
        """
        return self._SUBEXPRESSION(position, (self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._TERMINAL, "a"), (self._TERMINAL, "b"))), (self._TERMINAL, "c"))), (self._TERMINAL, "d"))), (self._TERMINAL, "e"))), (self._TERMINAL, "f"))), (self._TERMINAL, "g"))), (self._TERMINAL, "h"))), (self._TERMINAL, "i"))), (self._TERMINAL, "j"))), (self._TERMINAL, "k"))), (self._TERMINAL, "l"))), (self._TERMINAL, "m"))), (self._TERMINAL, "n"))), (self._TERMINAL, "o"))), (self._TERMINAL, "p"))), (self._TERMINAL, "q"))), (self._TERMINAL, "r"))), (self._TERMINAL, "s"))), (self._TERMINAL, "t"))), (self._TERMINAL, "u"))), (self._TERMINAL, "v"))), (self._TERMINAL, "w"))), (self._TERMINAL, "x"))), (self._TERMINAL, "y"))), (self._TERMINAL, "z"))))

    @cache
    def Num(self, position: int, dummy = None):
        """
        <Num> = "0"/"1"/"2"/"3"/"4"/"5"/"6"/"7"/"8"/"9" ;
        """
        return self._SUBEXPRESSION(position, (self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._TERMINAL, "0"), (self._TERMINAL, "1"))), (self._TERMINAL, "2"))), (self._TERMINAL, "3"))), (self._TERMINAL, "4"))), (self._TERMINAL, "5"))), (self._TERMINAL, "6"))), (self._TERMINAL, "7"))), (self._TERMINAL, "8"))), (self._TERMINAL, "9"))))

    @cache
    def Spaces(self, position: int, dummy = None):
        """
        <Spaces> = "\t"/"\r"/" " ;
        """
        return self._SUBEXPRESSION(position, (self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._TERMINAL, "\t"), (self._TERMINAL, "\r"))), (self._TERMINAL, " "))))

    @cache
    def Specials(self, position: int, dummy = None):
        """
        <Specials> = "+"/"*"/"-"/"&"/"!"/"?"/"<"/">"/'"'/"("/")"/"_"/","/"/"/";"/"="/"\\"/"#"/":"/"|"/"."/"'"/"%" ;
        """
        return self._SUBEXPRESSION(position, (self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._TERMINAL, "+"), (self._TERMINAL, "*"))), (self._TERMINAL, "-"))), (self._TERMINAL, "&"))), (self._TERMINAL, "!"))), (self._TERMINAL, "?"))), (self._TERMINAL, "<"))), (self._TERMINAL, ">"))), (self._TERMINAL, '"'))), (self._TERMINAL, "("))), (self._TERMINAL, ")"))), (self._TERMINAL, "_"))), (self._TERMINAL, ","))), (self._TERMINAL, "/"))), (self._TERMINAL, ";"))), (self._TERMINAL, "="))), (self._TERMINAL, '\\'))), (self._TERMINAL, "#"))), (self._TERMINAL, ":"))), (self._TERMINAL, "|"))), (self._TERMINAL, "."))), (self._TERMINAL, "'"))), (self._TERMINAL, "%"))))

    @cache
    def ASCII(self, position: int, dummy = None):
        """
        <ASCII> = <Alphabet_Lower>/<Alphabet_Upper>/<Num>/<Spaces>/<Specials> ;
        
        Need to update packratparsergenerator to allow e.g uint[0-27] rather than needing to write everything out manually 
        """
        return self._SUBEXPRESSION(position, (self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._VAR_NAME, (self.Alphabet_Lower, None)), (self._VAR_NAME, (self.Alphabet_Upper, None)))), (self._VAR_NAME, (self.Num, None)))), (self._VAR_NAME, (self.Spaces, None)))), (self._VAR_NAME, (self.Specials, None)))))

    @cache
    def newline(self, position: int, dummy = None):
        """
        <newline> = "\n" ;
        """
        return self._SUBEXPRESSION(position, (self._TERMINAL, "\n"))

    @cache
    def space(self, position: int, dummy = None):
        """
        <space> = " " ;
        """
        return self._SUBEXPRESSION(position, (self._TERMINAL, " "))

    @cache
    def whitespace(self, position: int, dummy = None):
        """
        <whitespace> = " "* ;
        """
        return self._SUBEXPRESSION(position, (self._ZERO_OR_MORE, (self._TERMINAL, " ")))

    @cache
    def equals(self, position: int, dummy = None):
        """
        <equals> = "=" ;
        """
        return self._SUBEXPRESSION(position, (self._TERMINAL, "="))

    @cache
    def underscore(self, position: int, dummy = None):
        """
        <underscore> = "_" ;
        """
        return self._SUBEXPRESSION(position, (self._TERMINAL, "_"))

    @cache
    def open_square_bracket(self, position: int, dummy = None):
        """
        <open_square_bracket> = "[" ;
        """
        return self._SUBEXPRESSION(position, (self._TERMINAL, "["))

    @cache
    def close_square_bracket(self, position: int, dummy = None):
        """
        <close_square_bracket> = "]" ;
        """
        return self._SUBEXPRESSION(position, (self._TERMINAL, "]"))

    @cache
    def open_bracket(self, position: int, dummy = None):
        """
        <open_bracket> = "(" ;
        """
        return self._SUBEXPRESSION(position, (self._TERMINAL, "("))

    @cache
    def close_bracket(self, position: int, dummy = None):
        """
        <close_bracket> = ")" ;
        """
        return self._SUBEXPRESSION(position, (self._TERMINAL, ")"))

    @cache
    def Is(self, position: int, dummy = None):
        """
        <Is> = "i", "s" ;
        """
        return self._SUBEXPRESSION(position, (self._SEQUENCE, ((self._TERMINAL, "i"), (self._TERMINAL, "s"))))

    @cache
    def comma(self, position: int, dummy = None):
        """
        <comma> = "," ;
        """
        return self._SUBEXPRESSION(position, (self._TERMINAL, ","))

    @cache
    def integer(self, position: int, dummy = None):
        """
        <integer> = "-"?, (((!"0", <Num>), <Num>*)/"0") ;
        """
        return self._SUBEXPRESSION(position, (self._SEQUENCE, ((self._OPTIONAL, (self._TERMINAL, "-")), (self._SUBEXPRESSION, (self._ORDERED_CHOICE, ((self._SUBEXPRESSION, (self._SEQUENCE, ((self._SUBEXPRESSION, (self._SEQUENCE, ((self._NOT_PREDICATE, (self._TERMINAL, "0")), (self._VAR_NAME, (self.Num, None))))), (self._ZERO_OR_MORE, (self._VAR_NAME, (self.Num, None)))))), (self._TERMINAL, "0")))))))

    @cache
    def variable(self, position: int, dummy = None):
        """
        <variable> = (<Alphabet_Lower>/<Alphabet_Upper>/"_"), (<Alphabet_Lower>/<Alphabet_Upper>/"_"/<Num>)* ;
        """
        return self._SUBEXPRESSION(position, (self._SEQUENCE, ((self._SUBEXPRESSION, (self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._VAR_NAME, (self.Alphabet_Lower, None)), (self._VAR_NAME, (self.Alphabet_Upper, None)))), (self._TERMINAL, "_")))), (self._ZERO_OR_MORE, (self._SUBEXPRESSION, (self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._VAR_NAME, (self.Alphabet_Lower, None)), (self._VAR_NAME, (self.Alphabet_Upper, None)))), (self._TERMINAL, "_"))), (self._VAR_NAME, (self.Num, None)))))))))

    @cache
    def line_terminator(self, position: int, dummy = None):
        """
        <line_terminator> = <whitespace>, <newline> ;
        """
        return self._SUBEXPRESSION(position, (self._SEQUENCE, ((self._VAR_NAME, (self.whitespace, None)), (self._VAR_NAME, (self.newline, None)))))

    @cache
    def size(self, position: int, dummy = None):
        """
        <size> = <integer> ;
        """
        return self._SUBEXPRESSION(position, (self._VAR_NAME, (self.integer, None)))

    @cache
    def quantity(self, position: int, dummy = None):
        """
        <quantity> = <integer> ;
        """
        return self._SUBEXPRESSION(position, (self._VAR_NAME, (self.integer, None)))

    @cache
    def memory_allocator(self, position: int, dummy = None):
        """
        <memory_allocator> = <type_identifier>, <underscore>, <size>, (<open_square_bracket>, <quantity>, <close_square_bracket>)? ;
        """
        return self._SUBEXPRESSION(position, (self._SEQUENCE, ((self._SEQUENCE, ((self._SEQUENCE, ((self._VAR_NAME, (self.type_identifier, None)), (self._VAR_NAME, (self.underscore, None)))), (self._VAR_NAME, (self.size, None)))), (self._OPTIONAL, (self._SUBEXPRESSION, (self._SEQUENCE, ((self._SEQUENCE, ((self._VAR_NAME, (self.open_square_bracket, None)), (self._VAR_NAME, (self.quantity, None)))), (self._VAR_NAME, (self.close_square_bracket, None)))))))))

    @cache
    def int_identifier(self, position: int, dummy = None):
        """
        <int_identifier> = "i", "n", "t" ;
        """
        return self._SUBEXPRESSION(position, (self._SEQUENCE, ((self._SEQUENCE, ((self._TERMINAL, "i"), (self._TERMINAL, "n"))), (self._TERMINAL, "t"))))

    @cache
    def float_identifier(self, position: int, dummy = None):
        """
        <float_identifier> = "f", "l", "o", "a", "t" ;
        """
        return self._SUBEXPRESSION(position, (self._SEQUENCE, ((self._SEQUENCE, ((self._SEQUENCE, ((self._SEQUENCE, ((self._TERMINAL, "f"), (self._TERMINAL, "l"))), (self._TERMINAL, "o"))), (self._TERMINAL, "a"))), (self._TERMINAL, "t"))))

    @cache
    def type_identifier(self, position: int, dummy = None):
        """
        <type_identifier> = <int_identifier>/<float_identifier> ;
        """
        return self._SUBEXPRESSION(position, (self._ORDERED_CHOICE, ((self._VAR_NAME, (self.int_identifier, None)), (self._VAR_NAME, (self.float_identifier, None)))))

    @cache
    def plus(self, position: int, dummy = None):
        """
        <plus> = "+" ;
        """
        return self._SUBEXPRESSION(position, (self._TERMINAL, "+"))

    @cache
    def minus(self, position: int, dummy = None):
        """
        <minus> = "-" ;
        """
        return self._SUBEXPRESSION(position, (self._TERMINAL, "-"))

    @cache
    def forward_slash(self, position: int, dummy = None):
        """
        <forward_slash> = "/" ;
        """
        return self._SUBEXPRESSION(position, (self._TERMINAL, "/"))

    @cache
    def star(self, position: int, dummy = None):
        """
        <star> = "*" ;
        """
        return self._SUBEXPRESSION(position, (self._TERMINAL, "*"))

    @cache
    def add(self, position: int, dummy = None):
        """
        <add> = (<variable>/<data>), <whitespace>, <plus>, <whitespace>, (<variable>/<data>) ;
        """
        return self._SUBEXPRESSION(position, (self._SEQUENCE, ((self._SEQUENCE, ((self._SEQUENCE, ((self._SEQUENCE, ((self._SUBEXPRESSION, (self._ORDERED_CHOICE, ((self._VAR_NAME, (self.variable, None)), (self._VAR_NAME, (self.data, None))))), (self._VAR_NAME, (self.whitespace, None)))), (self._VAR_NAME, (self.plus, None)))), (self._VAR_NAME, (self.whitespace, None)))), (self._SUBEXPRESSION, (self._ORDERED_CHOICE, ((self._VAR_NAME, (self.variable, None)), (self._VAR_NAME, (self.data, None))))))))

    @cache
    def subtract(self, position: int, dummy = None):
        """
        <subtract> = (<variable>/<data>), <whitespace>, <minus>, <whitespace>, (<variable>/<data>) ;
        """
        return self._SUBEXPRESSION(position, (self._SEQUENCE, ((self._SEQUENCE, ((self._SEQUENCE, ((self._SEQUENCE, ((self._SUBEXPRESSION, (self._ORDERED_CHOICE, ((self._VAR_NAME, (self.variable, None)), (self._VAR_NAME, (self.data, None))))), (self._VAR_NAME, (self.whitespace, None)))), (self._VAR_NAME, (self.minus, None)))), (self._VAR_NAME, (self.whitespace, None)))), (self._SUBEXPRESSION, (self._ORDERED_CHOICE, ((self._VAR_NAME, (self.variable, None)), (self._VAR_NAME, (self.data, None))))))))

    @cache
    def division(self, position: int, dummy = None):
        """
        <division> = (<variable>/<data>), <whitespace>, <forward_slash>, <whitespace>, (<variable>/<data>) ;
        """
        return self._SUBEXPRESSION(position, (self._SEQUENCE, ((self._SEQUENCE, ((self._SEQUENCE, ((self._SEQUENCE, ((self._SUBEXPRESSION, (self._ORDERED_CHOICE, ((self._VAR_NAME, (self.variable, None)), (self._VAR_NAME, (self.data, None))))), (self._VAR_NAME, (self.whitespace, None)))), (self._VAR_NAME, (self.forward_slash, None)))), (self._VAR_NAME, (self.whitespace, None)))), (self._SUBEXPRESSION, (self._ORDERED_CHOICE, ((self._VAR_NAME, (self.variable, None)), (self._VAR_NAME, (self.data, None))))))))

    @cache
    def multiplication(self, position: int, dummy = None):
        """
        <multiplication> = (<variable>/<data>), <whitespace>, <star>, <whitespace>, (<variable>/<data>) ;
        """
        return self._SUBEXPRESSION(position, (self._SEQUENCE, ((self._SEQUENCE, ((self._SEQUENCE, ((self._SEQUENCE, ((self._SUBEXPRESSION, (self._ORDERED_CHOICE, ((self._VAR_NAME, (self.variable, None)), (self._VAR_NAME, (self.data, None))))), (self._VAR_NAME, (self.whitespace, None)))), (self._VAR_NAME, (self.star, None)))), (self._VAR_NAME, (self.whitespace, None)))), (self._SUBEXPRESSION, (self._ORDERED_CHOICE, ((self._VAR_NAME, (self.variable, None)), (self._VAR_NAME, (self.data, None))))))))

    @cache
    def maths(self, position: int, dummy = None):
        """
        <maths> = <whitespace>, (<add>/<subtract>/<division>/<multiplication>), <whitespace> ;
        """
        return self._SUBEXPRESSION(position, (self._SEQUENCE, ((self._SEQUENCE, ((self._VAR_NAME, (self.whitespace, None)), (self._SUBEXPRESSION, (self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._ORDERED_CHOICE, ((self._VAR_NAME, (self.add, None)), (self._VAR_NAME, (self.subtract, None)))), (self._VAR_NAME, (self.division, None)))), (self._VAR_NAME, (self.multiplication, None))))))), (self._VAR_NAME, (self.whitespace, None)))))

    @cache
    def function_call(self, position: int, dummy = None):
        """
        <function_call> = <whitespace>, <variable>, <open_bracket>, ((<data>/<variable>)?, <whitespace>, (<comma>, <whitespace>, (<data>/<variable>), <whitespace>)*, <whitespace>)?, <close_bracket>, <whitespace> ;
        """
        return self._SUBEXPRESSION(position, (self._SEQUENCE, ((self._SEQUENCE, ((self._SEQUENCE, ((self._SEQUENCE, ((self._SEQUENCE, ((self._VAR_NAME, (self.whitespace, None)), (self._VAR_NAME, (self.variable, None)))), (self._VAR_NAME, (self.open_bracket, None)))), (self._OPTIONAL, (self._SUBEXPRESSION, (self._SEQUENCE, ((self._SEQUENCE, ((self._SEQUENCE, ((self._OPTIONAL, (self._SUBEXPRESSION, (self._ORDERED_CHOICE, ((self._VAR_NAME, (self.data, None)), (self._VAR_NAME, (self.variable, None)))))), (self._VAR_NAME, (self.whitespace, None)))), (self._ZERO_OR_MORE, (self._SUBEXPRESSION, (self._SEQUENCE, ((self._SEQUENCE, ((self._SEQUENCE, ((self._VAR_NAME, (self.comma, None)), (self._VAR_NAME, (self.whitespace, None)))), (self._SUBEXPRESSION, (self._ORDERED_CHOICE, ((self._VAR_NAME, (self.data, None)), (self._VAR_NAME, (self.variable, None))))))), (self._VAR_NAME, (self.whitespace, None)))))))), (self._VAR_NAME, (self.whitespace, None)))))))), (self._VAR_NAME, (self.close_bracket, None)))), (self._VAR_NAME, (self.whitespace, None)))))

    @cache
    def int(self, position: int, dummy = None):
        """
        <int> = <integer> ;
        """
        return self._SUBEXPRESSION(position, (self._VAR_NAME, (self.integer, None)))

    @cache
    def data(self, position: int, dummy = None):
        """
        <data> = <int> ;
        """
        return self._SUBEXPRESSION(position, (self._VAR_NAME, (self.int, None)))

    @cache
    def BSS_statement(self, position: int, dummy = None):
        """
        <BSS_statement> = <variable>, <whitespace>, <equals>, <whitespace>, <memory_allocator>, <line_terminator> ;
        """
        return self._SUBEXPRESSION(position, (self._SEQUENCE, ((self._SEQUENCE, ((self._SEQUENCE, ((self._SEQUENCE, ((self._SEQUENCE, ((self._VAR_NAME, (self.variable, None)), (self._VAR_NAME, (self.whitespace, None)))), (self._VAR_NAME, (self.equals, None)))), (self._VAR_NAME, (self.whitespace, None)))), (self._VAR_NAME, (self.memory_allocator, None)))), (self._VAR_NAME, (self.line_terminator, None)))))

    @cache
    def DATA_statement(self, position: int, dummy = None):
        """
        <DATA_statement> = <variable>, <whitespace>, <equals>, <whitespace>, <memory_allocator>, <space>, <Is>, <space>, <data>, <line_terminator> ;
        
         Rodata and data handling is same one is just readonly
        """
        return self._SUBEXPRESSION(position, (self._SEQUENCE, ((self._SEQUENCE, ((self._SEQUENCE, ((self._SEQUENCE, ((self._SEQUENCE, ((self._SEQUENCE, ((self._SEQUENCE, ((self._SEQUENCE, ((self._SEQUENCE, ((self._VAR_NAME, (self.variable, None)), (self._VAR_NAME, (self.whitespace, None)))), (self._VAR_NAME, (self.equals, None)))), (self._VAR_NAME, (self.whitespace, None)))), (self._VAR_NAME, (self.memory_allocator, None)))), (self._VAR_NAME, (self.space, None)))), (self._VAR_NAME, (self.Is, None)))), (self._VAR_NAME, (self.space, None)))), (self._VAR_NAME, (self.data, None)))), (self._VAR_NAME, (self.line_terminator, None)))))

    @cache
    def TEXT_statement(self, position: int, dummy = None):
        """
        <TEXT_statement> = <variable>, <whitespace>, <equals>, (<maths>/<function_call>), <line_terminator> ;
        """
        return self._SUBEXPRESSION(position, (self._SEQUENCE, ((self._SEQUENCE, ((self._SEQUENCE, ((self._SEQUENCE, ((self._VAR_NAME, (self.variable, None)), (self._VAR_NAME, (self.whitespace, None)))), (self._VAR_NAME, (self.equals, None)))), (self._SUBEXPRESSION, (self._ORDERED_CHOICE, ((self._VAR_NAME, (self.maths, None)), (self._VAR_NAME, (self.function_call, None))))))), (self._VAR_NAME, (self.line_terminator, None)))))

    @cache
    def RODATA_identifier(self, position: int, dummy = None):
        """
        <RODATA_identifier> = "R", "O", "D", "A", "T", "A" ;
        """
        return self._SUBEXPRESSION(position, (self._SEQUENCE, ((self._SEQUENCE, ((self._SEQUENCE, ((self._SEQUENCE, ((self._SEQUENCE, ((self._TERMINAL, "R"), (self._TERMINAL, "O"))), (self._TERMINAL, "D"))), (self._TERMINAL, "A"))), (self._TERMINAL, "T"))), (self._TERMINAL, "A"))))

    @cache
    def DATA_identifier(self, position: int, dummy = None):
        """
        <DATA_identifier> = "D", "A", "T", "A" ;
        """
        return self._SUBEXPRESSION(position, (self._SEQUENCE, ((self._SEQUENCE, ((self._SEQUENCE, ((self._TERMINAL, "D"), (self._TERMINAL, "A"))), (self._TERMINAL, "T"))), (self._TERMINAL, "A"))))

    @cache
    def BSS_identifier(self, position: int, dummy = None):
        """
        <BSS_identifier> = "B", "S", "S" ;
        """
        return self._SUBEXPRESSION(position, (self._SEQUENCE, ((self._SEQUENCE, ((self._TERMINAL, "B"), (self._TERMINAL, "S"))), (self._TERMINAL, "S"))))

    @cache
    def TEXT_identifier(self, position: int, dummy = None):
        """
        <TEXT_identifier> = "T", "E", "X", "T" ;
        """
        return self._SUBEXPRESSION(position, (self._SEQUENCE, ((self._SEQUENCE, ((self._SEQUENCE, ((self._TERMINAL, "T"), (self._TERMINAL, "E"))), (self._TERMINAL, "X"))), (self._TERMINAL, "T"))))

    @cache
    def RODATA(self, position: int, dummy = None):
        """
        <RODATA> = <RODATA_identifier>, <line_terminator>, (<DATA_statement>/<newline>)* ;
        """
        return self._SUBEXPRESSION(position, (self._SEQUENCE, ((self._SEQUENCE, ((self._VAR_NAME, (self.RODATA_identifier, None)), (self._VAR_NAME, (self.line_terminator, None)))), (self._ZERO_OR_MORE, (self._SUBEXPRESSION, (self._ORDERED_CHOICE, ((self._VAR_NAME, (self.DATA_statement, None)), (self._VAR_NAME, (self.newline, None)))))))))

    @cache
    def DATA(self, position: int, dummy = None):
        """
        <DATA> = <DATA_identifier>, <line_terminator>, (<DATA_statement>/<newline>)* ;
        """
        return self._SUBEXPRESSION(position, (self._SEQUENCE, ((self._SEQUENCE, ((self._VAR_NAME, (self.DATA_identifier, None)), (self._VAR_NAME, (self.line_terminator, None)))), (self._ZERO_OR_MORE, (self._SUBEXPRESSION, (self._ORDERED_CHOICE, ((self._VAR_NAME, (self.DATA_statement, None)), (self._VAR_NAME, (self.newline, None)))))))))

    @cache
    def BSS(self, position: int, dummy = None):
        """
        <BSS> = <BSS_identifier>, <line_terminator>, (<BSS_statement>/<newline>)* ;
        """
        return self._SUBEXPRESSION(position, (self._SEQUENCE, ((self._SEQUENCE, ((self._VAR_NAME, (self.BSS_identifier, None)), (self._VAR_NAME, (self.line_terminator, None)))), (self._ZERO_OR_MORE, (self._SUBEXPRESSION, (self._ORDERED_CHOICE, ((self._VAR_NAME, (self.BSS_statement, None)), (self._VAR_NAME, (self.newline, None)))))))))

    @cache
    def TEXT(self, position: int, dummy = None):
        """
        <TEXT> = <TEXT_identifier>, <line_terminator>, (<TEXT_statement>/<newline>)* ;
        """
        return self._SUBEXPRESSION(position, (self._SEQUENCE, ((self._SEQUENCE, ((self._VAR_NAME, (self.TEXT_identifier, None)), (self._VAR_NAME, (self.line_terminator, None)))), (self._ZERO_OR_MORE, (self._SUBEXPRESSION, (self._ORDERED_CHOICE, ((self._VAR_NAME, (self.TEXT_statement, None)), (self._VAR_NAME, (self.newline, None)))))))))

    @cache
    def grammar(self, position: int, dummy = None):
        """
        <grammar> = <DATA>?, <newline>*, <RODATA>?, <newline>*, <BSS>?, <newline>*, <TEXT>, <newline>* ;
        """
        return self._SUBEXPRESSION(position, (self._SEQUENCE, ((self._SEQUENCE, ((self._SEQUENCE, ((self._SEQUENCE, ((self._SEQUENCE, ((self._SEQUENCE, ((self._SEQUENCE, ((self._OPTIONAL, (self._VAR_NAME, (self.DATA, None))), (self._ZERO_OR_MORE, (self._VAR_NAME, (self.newline, None))))), (self._OPTIONAL, (self._VAR_NAME, (self.RODATA, None))))), (self._ZERO_OR_MORE, (self._VAR_NAME, (self.newline, None))))), (self._OPTIONAL, (self._VAR_NAME, (self.BSS, None))))), (self._ZERO_OR_MORE, (self._VAR_NAME, (self.newline, None))))), (self._VAR_NAME, (self.TEXT, None)))), (self._ZERO_OR_MORE, (self._VAR_NAME, (self.newline, None))))))