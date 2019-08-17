from xavium.commands import op
from xedis.store import STORE
from xedis.utils import get_size, get_signature


@op
def flush():
    STORE.clear()


@op
def info():
    num_items = len(STORE)
    mem_usage = get_size(STORE)
    return {'num_items': num_items, 'mem_usage': mem_usage}


@op
def help(cmd=None):
    from xedis.parser import COMMANDS

    if cmd is None:
        cmds = sorted([c for c in COMMANDS if not c.startswith('_')])
        return '\n'.join(map(get_signature, cmds))
    else:
        return get_signature(cmd)


@op
def keys():
    return STORE.keys()


@op
def rem(name):
    del STORE[name]


@op
def screate(name):
    STORE[name] = set()


@op
def sget(name):
    return STORE[name]


@op(parallelizable=True)
def sadd(name, item):
    STORE[name].add(item)


@op
def srem(name, *items):
    for item in items:
        STORE[name].remove(item)


@op
def sinter(*names):
    result = STORE[names[0]]
    for name in names[1:]:
        result = result.intersection(STORE[name])
    return result


@op
def sunion(*names):
    result = STORE[names[0]]
    for name in names[1:]:
        result = result.union(STORE[name])
    return result


@op
def scount(name):
    return len(STORE[name])


@op
def lcreate(name):
    STORE[name] = []


@op
def lappend(name, *items):
    STORE[name].extend(items)


@op
def lget(name):
    return STORE[name]


@op
def lrem(name, *items):
    for item in items:
        STORE[name].remove(item)


@op
def lcount(name):
    return len(STORE[name])


@op
def hcreate(name):
    STORE[name] = {}


@op
def hset(name, *items):
    for item in items:
        k, v = item.split(':')
        STORE[name][k] = v


@op(parallelizable=True)
def hpop(name, item):
    del STORE[name][item]


@op
def hkeys(name):
    return STORE[name].keys()


@op
def hvalues(name):
    return STORE[name].values()


@op(parallelizable=True)
def hget(name, item):
    return STORE[name][item]


@op
def hcount(name):
    return len(STORE[name])
