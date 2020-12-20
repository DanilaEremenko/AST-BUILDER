from uuid import uuid1

LIST_STR = '[list]'


def get_uuid():
    return uuid1().hex


def draw_and_connect(ast_gv_str, parent_uuid, child_uuid, child_name, connect_name):
    ast_gv_str[0] += f"{child_uuid} [label = \"{child_name}\"]\n"
    ast_gv_str[0] += f"{parent_uuid} -> {child_uuid} [label = {connect_name}]\n"
    return child_uuid


def dict_to_gv_recurs(ast_dict, ast_gv_res):
    if ast_dict['type'] == 'num':
        draw_and_connect(
            ast_gv_str=ast_gv_res,
            parent_uuid=ast_dict['uuid'],
            child_uuid=get_uuid(),
            child_name=ast_dict['n'],
            connect_name='n'
        )
        return
    elif ast_dict['type'] == 'ident':
        draw_and_connect(
            ast_gv_str=ast_gv_res,
            parent_uuid=ast_dict['uuid'],
            child_uuid=get_uuid(),
            child_name=ast_dict['id'],
            connect_name='id'
        )
        draw_and_connect(
            ast_gv_str=ast_gv_res,
            parent_uuid=ast_dict['uuid'],
            child_uuid=get_uuid(),
            child_name=ast_dict['ctx'],
            connect_name='ctx'
        )
        return

    for key, value in ast_dict.items():
        if type(value) == list:
            new_list_uuid = draw_and_connect(
                ast_gv_str=ast_gv_res,
                parent_uuid=ast_dict['uuid'],
                child_uuid=get_uuid(),
                child_name=LIST_STR,
                connect_name=key
            )

            for i, list_elem in enumerate(value):
                # create element if list
                draw_and_connect(
                    ast_gv_str=ast_gv_res,
                    parent_uuid=new_list_uuid,
                    child_uuid=list_elem['uuid'],
                    child_name=list_elem['type'],
                    connect_name=str(i)
                )
                # process child
                dict_to_gv_recurs(list_elem, ast_gv_res)

        elif type(value) == str:
            pass

        elif type(value) == dict:
            raise Exception('Wha?')

        else:
            raise Exception('Wha?')


def ast_dict_to_gv(ast_dict):
    ast_gv_res = ['digraph G {\n']
    dict_to_gv_recurs(ast_dict=ast_dict, ast_gv_res=ast_gv_res)
    return ast_gv_res[0] + '}'


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
    ast_gv_str = ast_dict_to_gv(ast_dict)
    print(ast_gv_str)


if __name__ == '__main__':
    test()
