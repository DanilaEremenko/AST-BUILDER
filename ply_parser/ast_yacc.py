from ast_dict_getters import *
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
def p_statements_trash(p):
    """statements : statements NEWLINE
    """
    p[0] = p[1]


def p_statements(p):
    """statements : statements statement
                |   statement
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = [*p[1], p[2]]


def p_statement(p):
    """statement : compound_stmt
                |  simple_stmt
    """
    p[0] = p[1]


def p_compound_stmt(p):
    """compound_stmt : if_stmt
                |      while_stmt
    """
    p[0] = p[1]


def p_simple_stmt(p):
    """simple_stmt : simple_stmt small_stmt NEWLINE
                |    small_stmt NEWLINE
    """
    if len(p) == 4:
        if type(p[1]) == list:
            p[0] = [*p[1], p[2]]
        elif type(p[1]) == dict:
            p[0] = [p[1], p[2]]
    else:
        p[0] = p[1]


def p_small_stmt(p):
    """small_stmt : set_value
                |  PASS
                |  BREAK
                |  CONTINUE
    """
    p[0] = p[1]


def p_block(p):
    """block : LBRACE statements RBRACE
            |  LBRACE statements NEWLINE RBRACE
            |  NEWLINE LBRACE statements RBRACE
            |  NEWLINE LBRACE  statements NEWLINE RBRACE
            |  LBRACE  NEWLINE statements RBRACE
            |  LBRACE  NEWLINE statements NEWLINE RBRACE
            |  NEWLINE LBRACE  NEWLINE statements RBRACE
            |  NEWLINE LBRACE  NEWLINE statements NEWLINE RBRACE
            |  simple_stmt
    """
    for token in p:
        if type(token) == list:
            p[0] = token
            break


#############################################################
# ---------------------- WHILE ------------------------------
#############################################################
def p_while_stmt(p):
    """while_stmt : WHILE compare_chain ':' block else_block
                |   WHILE compare_chain ':' block
    """


#############################################################
# ---------------------- CONDITION --------------------------
#############################################################
def p_if_stmt(p):
    """if_stmt : IF compare_chain block elif_stmt
            |    IF compare_chain block else_block
            |    IF compare_chain block
    """
    if len(p) == 5:
        p[0] = get_if_dict(test=p[2], body=p[3], orelse=p[4])
    else:
        p[0] = get_if_dict(test=p[2], body=p[3], orelse=[])


def p_elif_stmt(p):
    """elif_stmt : ELIF compare_chain ':' block elif_stmt
            |      ELIF compare_chain ':' block else_block
            |      ELIF compare_chain ':' block
    """


def p_else_block(p):
    """else_block : ELSE ':' block
    """


def p_compare_chain_add(p):
    """compare_chain : compare_chain LT bin_op
                   |   compare_chain GT bin_op
                   |   compare_chain LT_EQ bin_op
                   |   compare_chain GT_EQ bin_op
                   |   compare_chain NOT_EQ bin_op
                   |   compare_chain EQ bin_op
     """
    p[0] = {**p[1]}
    p[0]['ops'].append(p[2])
    p[0]['comparators'].append(p[3])


def p_compare_chain_init(p):
    """compare_chain : bin_op LT bin_op
                   |   bin_op GT bin_op
                   |   bin_op LT_EQ bin_op
                   |   bin_op GT_EQ bin_op
                   |   bin_op NOT_EQ bin_op
                   |   bin_op EQ bin_op
     """
    p[0] = get_compare_dict(left=p[1], ops=[p[2]], comparators=[p[3]])


#############################################################
# ---------------------- BIN_OP -----------------------------
#############################################################
def p_div_bin_op_with_bin_op(p):
    """bin_op : bin_op TIMES bin_op
            |   bin_op DIV bin_op"""
    p[0] = get_bin_op_dict(left=p[1], op=p[2], right=p[3])


def p_bin_op_with_bin_op(p):
    """bin_op : bin_op MINUS bin_op
            |   bin_op PLUS bin_op"""
    p[0] = get_bin_op_dict(left=p[1], op=p[2], right=p[3])


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
    """set_value : ident_list EQUAL_SET value_list"""
    p[0] = get_set_value_dict(targets=p[1], values=p[3])


def p_value_list(p):
    """value_list : value_list COMMA bin_op
                    | bin_op
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
