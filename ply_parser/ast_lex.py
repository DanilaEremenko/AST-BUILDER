from ast_dict_getters import get_str_dict, get_ident_dict, get_empty_node_dict, get_num_dict
from ply import lex
import re

#######################################################################
# --------------------------- LEX -------------------------------------
#######################################################################
tokens = (
    'IDENT',

    # LOGIC
    'AND',
    'OR',

    # BINARY_OP
    'PLUS',
    'MINUS',
    'TIMES',
    'DIV',

    'LPAREN',
    'RPAREN',

    'LBRACKET',
    'RBRACKET',

    # SET VALUE
    'COMMA',
    'EQUAL_SET',

    # TYPES
    'NUM',
    'STR',

    # BODY
    'LBRACE',
    'RBRACE',

    # OPERATORS
    'FOR',
    'WHILE',
    'IF',
    'ELSE',
    'ELIF',

    'PASS',
    'BREAK',
    'CONTINUE',
    'IN',

    # COMMENT
    'COMMENT',
    'NEWLINE',

    # COMPARE
    'LT',
    'GT',
    'LT_EQ',
    'GT_EQ',
    'NOT_EQ',
    'EQ'

)

reserved = {
    'for': 'FOR',
    'while': 'WHILE',

    'if': 'IF',
    'elif': 'ELIF',
    'else': 'ELSE',

    'pass': 'PASS',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'in': 'IN',

    'and': 'AND',
    'or': 'OR',

    '+': 'PLUS',
    '-': 'MINUS',
    '*': 'TIMES',
    '/': 'DIV',
    '&': 'AND',
    '|': 'OR',

    '<': 'LT',
    '>': 'GT',
    '<=': 'LT_EQ',
    '>=': 'GT_EQ',
    '!=': 'NOT_EQ',
    '==': 'EQ'

}

# COMMON
t_ignore = ' \t'

# MATH
t_COMMA = r'\,'


def t_BIN_OPS(t):
    r'\-|\+|\*|\/|\&|\|'
    t.type = reserved[t.value]
    t.value = get_empty_node_dict(type=t.type.lower())
    return t


# COMPARE
def t_COMPARE_OPS(t):
    r'\<|\<=|\>|\>=|==|\!='
    t.type = reserved[t.value]
    t.value = get_empty_node_dict(type=t.type.lower())
    return t


t_EQUAL_SET = r'\='

t_LPAREN = r'\('
t_RPAREN = r'\)'

t_LBRACKET = r'\['
t_RBRACKET = r'\]'

t_LBRACE = r'\{'
t_RBRACE = r'\}'


def t_COMMENT(t):
    r'\#.*'


def t_IDENT(t):
    r'[a-zA-Z]+[_a-zA-Z0-9]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    else:
        t.value = get_ident_dict(id=t.value, ctx='store')
    return t


# TYPES
def t_NUM(t):
    r'[0-9]+'
    t.value = get_num_dict(n=int(t.value))
    return t


def t_STR(t):
    r'\".+\"|\'.+\''
    t.value = get_str_dict(s=t.value[1:-1])
    return t


def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    return t


def t_error(t):
    print("Invalid Token:", t.value[0])
    t.lexer.skip(1)


lexer = lex.lex(reflags=re.UNICODE | re.VERBOSE)
