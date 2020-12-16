from ply import lex
import ply.yacc as yacc
import re
import uuid

#######################################################################
# --------------------------- LEX -------------------------------------
#######################################################################
tokens = (
    'IDENT',

    # MATH
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


# TYPES
def t_NUM(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t


def t_IDENT(t):
    r'[a-zA-Z]+[_a-zA-Z0-9]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t


def t_STR(t):
    r'\'[_a-zA-Z][_a-zA-Z0-9]\'|\"[_a-zA-Z][_a-zA-Z0-9]\"'
    t.value = int(t.value)
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


#######################################################################
# --------------------------- YACC ------------------------------------
#######################################################################
def p_module(p):
    """module : lines"""


def p_body(p):
    """body : LBRACE lines RBRACE"""
    p[0] = p[2]


def p_lines(p):
    """lines : lines line
            | line
    """


def p_line(p):
    """line : set_value
            | expr
            | while_expr
            | condition_expr
            | COMMENT
    """


def p_condition_expr(p):
    """condition_expr :   condition_expr ELSE body
                        | condition_expr ELIF LPAREN expr RPAREN body
                        | IF LPAREN expr RPAREN body

    """


def p_while_expr(p):
    """while_expr : WHILE expr body

    """


def p_set_value(p):
    """set_value : IDENT EQUAL NUM"""
    p[0] = p[3]


def p_add(p):
    """expr : expr PLUS expr"""
    p[0] = p[1] + p[3]


def p_sub(p):
    """expr : expr MINUS expr"""
    p[0] = p[1] - p[3]


def p_mult(p):
    """expr : expr DIV expr"""
    if p[3] == 0:
        print("Can't divide by 0")
        raise ZeroDivisionError('integer division by 0')
    p[0] = p[1] / p[3]


def p_div(p):
    """expr : expr TIMES expr"""
    p[0] = p[1] * p[3]


def p_SIGNMINUS_TO_EXPR(p):
    """expr : MINUS expr %prec UMINUS"""
    p[0] = - p[2]


def p_NUM_TO_EXPR(p):
    """expr : NUM
            | IDENT"""
    p[0] = str(p[1])


def p_compare_op(p):
    """compare_op : LESS
                | MORE
                | NOT EQUAL
                | EQUAL EQUAL
                | AND
                | OR"""
    p[0] = ''.join(p[1:])


def p_COMPARE_TO_EXPR(p):
    """expr : expr compare_op expr"""
    p[0] = p[1] + p[3]


def p_PARENS_TO_EXPR(p):
    """expr : LPAREN expr RPAREN"""
    p[0] = p[2]


def p_error(p):
    print("Syntax error in input!")
    print(str(p))


precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIV'),
    ('nonassoc', 'UMINUS')
)

parser = yacc.yacc()

graph_str = ''

with open('1_input_math.txt') as input_fp:
    input_code = input_fp.read()

res = parser.parse(input_code, debug=True)  # the input

graph_str = 'diagraph G {' + graph_str + '}'
with open('result.gv','w') as result_fp:
    result_fp.write(graph_str)
