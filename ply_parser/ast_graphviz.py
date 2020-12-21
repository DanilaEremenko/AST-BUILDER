from graphviz import Digraph

from ast_dict_getters import get_uuid

LIST_STR = '[list]'


def draw_and_connect(ast_digraph: Digraph, parent_uuid, child_uuid, child_name, connect_name):
    # ast_gv_str[0] += f"{child_uuid} [label = \"{child_name}\"]\n"
    # ast_gv_str[0] += f"{parent_uuid} -> {child_uuid} [label = {connect_name}]\n"
    try:
        ast_digraph.node(name=child_uuid, label=child_name)
        ast_digraph.edge(tail_name=parent_uuid, head_name=child_uuid, label=connect_name)
        return child_uuid
    except Exception():
        print()


def dict_to_gv_recurs(ast_dict: dict, ast_digraph: Digraph):
    for key, value in ast_dict.items():
        if type(value) == list:
            # draw [list] node
            new_list_uuid = draw_and_connect(
                ast_digraph=ast_digraph,
                parent_uuid=ast_dict['uuid'],
                child_uuid=get_uuid(),
                child_name=LIST_STR,
                connect_name=key
            )

            for i, list_elem in enumerate(value):
                # create elements if list
                draw_and_connect(
                    ast_digraph=ast_digraph,
                    parent_uuid=new_list_uuid,
                    child_uuid=list_elem['uuid'],
                    child_name=list_elem['type'],
                    connect_name=str(i)
                )
                # process child
                dict_to_gv_recurs(list_elem, ast_digraph)

        elif type(value) == str and key not in ('type', 'uuid'):
            draw_and_connect(
                ast_digraph=ast_digraph,
                parent_uuid=ast_dict['uuid'],
                child_uuid=get_uuid(),
                child_name=value,
                connect_name=key
            )
        elif type(value) == int:
            draw_and_connect(
                ast_digraph=ast_digraph,
                parent_uuid=ast_dict['uuid'],
                child_uuid=get_uuid(),
                child_name=str(value),
                connect_name=key
            )
        elif type(value) == dict:
            draw_and_connect(
                ast_digraph=ast_digraph,
                parent_uuid=ast_dict['uuid'],
                child_uuid=value['uuid'],
                child_name=value['type'],
                connect_name=key
            )
            dict_to_gv_recurs(value, ast_digraph)


def ast_dict_to_gv(ast_dict):
    ast_digraph = Digraph(format='pdf')
    dict_to_gv_recurs(ast_dict=ast_dict, ast_digraph=ast_digraph)
    return ast_digraph


def test():
    ast_dict = {
        'type': 'module',
        'uuid': get_uuid(),
        'body': [
            {
                'type': 'assign',
                'uuid': get_uuid(),
                'targets': [
                    {
                        'type': 'ident',
                        'uuid': get_uuid(),
                        'id': 'a',
                        'ctx': 'store'
                    },
                    {
                        'type': 'ident',
                        'uuid': get_uuid(),
                        'id': 'b',
                        'ctx': 'store'

                    }
                ],
                'values': [
                    {
                        'type': 'num',
                        'uuid': get_uuid(),
                        'n': 5
                    },
                    {
                        'type': 'num',
                        'uuid': get_uuid(),
                        'n': 6
                    },

                ]
            }
        ]

    }
    ast_digraph = ast_dict_to_gv(ast_dict)
    ast_digraph.view(filename='result.gv')


if __name__ == '__main__':
    test()
