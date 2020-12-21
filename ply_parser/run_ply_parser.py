from ast_yacc import parser
from ast_graphviz import ast_dict_to_gv, get_uuid

if __name__ == '__main__':
    with open('1_input_math.txt') as input_fp:
        input_code = input_fp.read()

    ast_lines_dict = parser.parse(input_code, debug=True)  # the input
    ast_dict = {
        'type': 'module',
        'uuid': get_uuid(),
        'body': ast_lines_dict
    }
    ast_digraph = ast_dict_to_gv(ast_dict=ast_dict)
    ast_digraph.view(filename='result.gv')
