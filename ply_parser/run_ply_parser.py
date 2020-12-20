from ast_yacc import parser
from ast_graphviz import ast_dict_to_gv

if __name__ == '__main__':
    with open('1_input_math.txt') as input_fp:
        input_code = input_fp.read()

    ast_dict = parser.parse(input_code, debug=True)  # the input
    ast_gv_str = ast_dict_to_gv(ast_dict=ast_dict)

    with open('result.gv', 'w') as result_fp:
        result_fp.write(ast_gv_str)
