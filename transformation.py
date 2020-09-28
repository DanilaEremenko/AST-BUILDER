import ast
import re


def get_transformed_ast(code):
    code_ast = ast.parse(code)
    transformed_ast = transform_ast(code_ast)
    return transformed_ast


def transform_ast(code_ast):
    if isinstance(code_ast, ast.AST):
        node = {to_camelcase(k): transform_ast(getattr(code_ast, k)) for k in code_ast._fields}
        node['node_type'] = to_camelcase(code_ast.__class__.__name__)
        return node
    elif isinstance(code_ast, list):
        return [transform_ast(el) for el in code_ast]
    else:
        return code_ast


def to_camelcase(string):
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', string).lower()
