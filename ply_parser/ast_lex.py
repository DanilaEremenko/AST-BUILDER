from ast_dict_getters import get_str_dict, get_ident_dict, get_empty_node_dict
from ply import lex
import re

#######################################################################
# --------------------------- LEX -------------------------------------
#######################################################################
tokens = (
    'IDENT',

    # MATH
    'COMMA',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIV',

    # COMPARE
    'LESS',
    'MORE',
    'NOT',
    'EQUAL',
    'AND',
    'OR',

    # TYPES
    'NUM',

    # # BODY
    # 'LBRACE',
    # 'RBRACE',
    'LPAREN',
    'RPAREN',
    #
    # # OPERATORS
    # 'WHILE',
    # 'IF',
    # 'ELSE',
    # 'ELIF',

    # COMMENT
    'COMMENT',
    'NEXT_LINE'

)

reserved = {
    'while': 'WHILE',
    'if': 'IF',
    'elif': 'ELIF',
    'else': 'ELSE',
    '+': 'PLUS',
    '-': 'MINUS',
    '*': 'TIMES',
    '/': 'DIV',
    '&': 'AND',
    '|': 'OR',
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
t_LESS = r'\<'
t_MORE = r'\>'
t_NOT = r'\!'
t_EQUAL = r'\='


def t_COMMENT(t):
    r'\#.*'
    t.value = 'COMMENT'


def t_IDENT(t):
    r'[a-zA-Z]+[_a-zA-Z0-9]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    t.value = get_ident_dict(id=t.value, ctx='store')
    return t


# TYPES
def t_NUM(t):
    r'[0-9]+'
    t.value = get_str_dict(int(t.value))
    return t


def t_STR(t):
    r'\'[_a-zA-Z][_a-zA-Z0-9]\'|\"[_a-zA-Z][_a-zA-Z0-9]\"'
    t.value = get_str_dict(str_val=t.value)
    return t


# BODY
# t_LBRACE = r'\{'
# t_RBRACE = r'\}'
#
# t_LPAREN = r'\('
# t_RPAREN = r'\)'


def t_NEXT_LINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    return t


def t_error(t):
    print("Invalid Token:", t.value[0])
    t.lexer.skip(1)


lexer = lex.lex(reflags=re.UNICODE | re.VERBOSE)
