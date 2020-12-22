RANDOM = 0


def get_uuid():
    # from uuid import uuid1
    # return uuid1().hex # TODO excuse me???
    global RANDOM
    RANDOM += 1
    return str(RANDOM)


def get_empty_node_dict(type, uuid=None):
    if uuid is None: uuid = get_uuid()
    return {'type': type, 'uuid': uuid}


def get_list_comprehension_dict(operation, generators: list, uuid=None):
    if uuid is None: uuid = get_uuid()
    return {'type': 'list_comprehension', 'uuid': uuid, 'operation': operation, 'generators': generators}


def get_comprehension(target, iter, ifs: list, uuid=None):
    if uuid is None: uuid = get_uuid()
    return {'type': 'comprehension', 'uuid': uuid, 'target': target, 'iter': iter, 'ifs': ifs}  # TODO is async


def get_list(values: list, ctx, uuid=None):
    if uuid is None: uuid = get_uuid()
    return {'type': 'list', 'uuid': uuid, 'values': values, 'ctx': ctx}


def get_while_dict(test, body: list, orelse: list, uuid=None):
    if uuid is None: uuid = get_uuid()
    return {'type': 'while', 'uuid': uuid, 'test': test, 'body': body, 'orelse': orelse}


def get_if_dict(test, body: list, orelse: list, uuid=None):
    if uuid is None: uuid = get_uuid()
    return {'type': 'if', 'uuid': uuid, 'test': test, 'body': body, 'orelse': orelse}


def get_bool_op_dict(op: str, values: list, uuid=None):
    if uuid is None: uuid = get_uuid()
    return {'type': 'bool_op', 'uuid': uuid, 'op': op, 'values': values}


def get_compare_dict(left, ops: list, comparators: list, uuid=None):
    if uuid is None: uuid = get_uuid()
    return {'type': 'compare', 'uuid': uuid, 'left': left, 'ops': ops, 'comparators': comparators}


def get_bin_op_dict(left, op, right, uuid=None):
    if uuid is None: uuid = get_uuid()
    return {'type': 'bin_op', 'uuid': uuid, 'left': left, 'op': op, 'right': right}


def get_set_value_dict(targets: list, values: list, uuid=None):
    if uuid is None: uuid = get_uuid()
    return {'type': 'assign', 'uuid': uuid, 'targets': targets, 'values': values}


def get_func_call_dict(func, args: list, keywords: list, uuid=None):
    if uuid is None: uuid = get_uuid()
    return {'type': 'func_call', 'uuid': uuid, 'func': func, 'args': args, 'keywords': keywords}


def get_ident_dict(id, ctx, uuid=None):
    if uuid is None: uuid = get_uuid()
    return {'type': 'ident', 'uuid': uuid, 'id': id, 'ctx': ctx}


def get_num_dict(n, uuid=None):
    if uuid is None: uuid = get_uuid()
    return {'type': 'num', 'uuid': uuid, 'n': n}


def get_str_dict(s, uuid=None):
    if uuid is None: uuid = get_uuid()
    return {'type': 'str', 'uuid': uuid, 's': s}
