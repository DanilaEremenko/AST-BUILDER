RANDOM = 0


def get_uuid():
    # from uuid import uuid1
    # return uuid1().hex # TODO excuse me???
    global RANDOM
    RANDOM += 1
    return str(RANDOM)


def get_empty_node_dict(type, uuid=None):
    if uuid is None:
        uuid = get_uuid()
    return {'type': type, 'uuid': uuid}


def get_bin_op_dict(left, op, right, uuid=None):
    if uuid is None:
        uuid = get_uuid()
    return {'type': 'bin_op', 'uuid': uuid, 'left': left, 'op': op, 'right': right}


def get_ident_dict(id, ctx, uuid=None):
    if uuid is None:
        uuid = get_uuid()
    return {'type': 'ident', 'uuid': uuid, 'id': id, 'ctx': ctx}


def get_num_dict(n, uuid=None):
    if uuid is None:
        uuid = get_uuid()
    return {'type': 'str', 'uuid': uuid, 'n': n}


def get_str_dict(str_val, uuid=None):
    if uuid is None:
        uuid = get_uuid()
    return {'type': 'num', 'uuid': uuid, 'str': str_val}
