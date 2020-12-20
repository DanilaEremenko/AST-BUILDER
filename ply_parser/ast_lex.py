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

    # BODY
    'LBRACE',
    'RBRACE',
    'LPAREN',
    'RPAREN',

    # OPERATORS
    'WHILE',
    'IF',
    'ELSE',
    'ELIF',

    # COMMENT
    'COMMENT'

)

# COMMON
t_ignore = ' \t'

t_COMMENT = r'\#.*'

# MATH
t_COMMA = r'\,'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIV = r'\/'
t_AND = r'\&'
t_OR = r'\|'

# COMPARE
t_LESS = r'\<'
t_MORE = r'\>'
t_NOT = r'\!'
t_EQUAL = r'\='

reserved = {
    'while': 'WHILE',
    'if': 'IF',
    'elif': 'ELIF',
    'else': 'ELSE'
}


def t_IDENT(t):
    r'[a-zA-Z]+[_a-zA-Z0-9]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    t.value = {'id': t.value, 'ctx': 'store'}
    return t


# TYPES
def t_NUM(t):
    r'[0-9]+'
    t.value = {'n': int(t.value)}
    return t


def t_STR(t):
    r'\'[_a-zA-Z][_a-zA-Z0-9]\'|\"[_a-zA-Z][_a-zA-Z0-9]\"'
    t.value = {'str': t.value}
    return t


# BODY
t_LBRACE = r'\{'
t_RBRACE = r'\}'

t_LPAREN = r'\('
t_RPAREN = r'\)'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Invalid Token:", t.value[0])
    t.lexer.skip(1)


lexer = lex.lex(reflags=re.UNICODE | re.VERBOSE)
