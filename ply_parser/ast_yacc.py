from ast_lex import tokens
from ast_graphviz import get_uuid
import ply.yacc as yacc

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIV'),
    ('nonassoc', 'UMINUS')
)


#######################################################################
# --------------------------- YACC ------------------------------------
#######################################################################
def p_lines(p):
    """lines : lines NEXT_LINE line
            | line
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [*p[1], p[3]]


def p_line(p):
    """line : set_value
            | expr
            | COMMENT
    """
    p[0] = p[1]


#############################################################
# ---------------------- COMPARE ----------------------------
#############################################################
def p_compare_op(p):
    """compare_op : LESS
                | MORE
                | NOT EQUAL
                | EQUAL EQUAL
                | AND
                | OR"""


def p_COMPARE_TO_EXPR(p):
    """expr : expr compare_op expr"""


def p_PARENS_TO_EXPR(p):
    """expr : LPAREN expr RPAREN"""


#############################################################
# ---------------------- BIN_OP -----------------------------
#############################################################
def p_bin_ops_to_expr(p):
    """expr : bin_op"""
    p[0] = {'type': 'expression', 'uuid': get_uuid(), 'val': p[1]}


def p_div_bin_op_with_bin_op(p):
    """bin_op : bin_op TIMES bin_op
            |   bin_op DIV bin_op"""
    p[0] = {'type': 'bin_op', 'uuid': get_uuid(), 'left': p[1], 'op': p[2], 'right': p[3]}


def p_bin_op_with_bin_op(p):
    """bin_op : bin_op MINUS bin_op
            |   bin_op PLUS bin_op"""
    p[0] = {'type': 'bin_op', 'uuid': get_uuid(), 'left': p[1], 'op': p[2], 'right': p[3]}


def p_expr2uminus(p):
    'bin_op : MINUS bin_op %prec UMINUS'
    p[0] = {'type': 'unary_op', 'uuid': get_uuid(), 'op': 'usub', 'operand': p[2]}


def p_parens(p):
    'bin_op : LPAREN bin_op RPAREN'
    p[0] = p[2]


def p_operand_ident(p):
    """bin_op : IDENT"""
    p[0] = {**p[1], 'ctx': 'load'}


def p_operand_num(p):
    """bin_op : NUM"""
    p[0] = p[1]


#############################################################
# ---------------------- SET VALUE --------------------------
#############################################################
def p_set_value(p):
    """set_value : ident_list EQUAL value_list"""
    p[0] = {
        'type': 'assign',
        'uuid': get_uuid(),
        'targets': p[1],
        'values': p[3]
    }


def p_value_list(p):
    """value_list : value_list  COMMA IDENT
                    | value_list  COMMA NUM
                    | IDENT
                    | NUM
                """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [*p[1], p[3]]


def p_ident_list(p):
    """ident_list : ident_list  COMMA IDENT
                    | IDENT
                """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [*p[1], p[3]]


def p_error(p):
    print("Syntax error in input!")
    print(str(p))


parser = yacc.yacc()
