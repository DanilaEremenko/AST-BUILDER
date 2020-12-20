from ast_lex import tokens
import ply.yacc as yacc


#######################################################################
# --------------------------- YACC ------------------------------------
#######################################################################
def p_module(p):
    """module : lines"""
    p[0] = {'who': 'me'}


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


def p_sub(p):
    """expr : expr MINUS expr"""


def p_mult(p):
    """expr : expr DIV expr"""


def p_div(p):
    """expr : expr TIMES expr"""


def p_SIGNMINUS_TO_EXPR(p):
    """expr : MINUS expr %prec UMINUS"""


def p_VALUE_LIST(p):
    """p_VALUE_LIST : ident_list  COMMA IDENT
                    | ident_list  COMMA NUM
                    | IDENT
                    | NUM
                """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0].append(p[3])


def p_IDENT_LIST(p):
    """ident_list : ident_list  COMMA IDENT
                | IDENT
            """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0].append(p[3])


def p_NUM_TO_EXPR(p):
    """expr : NUM
            | IDENT"""


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


def p_error(p):
    print("Syntax error in input!")
    print(str(p))


precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIV'),
    ('nonassoc', 'UMINUS')
)

parser = yacc.yacc()
