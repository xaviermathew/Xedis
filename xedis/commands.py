from xedis.store import STORE
from xedis.utils import get_size, get_signature


def flush():
    STORE.clear()


def info():
    num_items = len(STORE)
    mem_usage = get_size(STORE)
    return {'num_items': num_items, 'mem_usage': mem_usage}


def help(cmd=None):
    from xedis.parser import COMMANDS

    if cmd is None:
        cmds = sorted([c for c in COMMANDS if not c.startswith('_')])
        return '\n'.join(map(get_signature, cmds))
    else:
        return get_signature(cmd)


def keys():
    return STORE.keys()


def rem(name):
    del STORE[name]


def screate(name):
    STORE[name] = set()


def sget(name):
    return STORE[name]


def sadd(name, *items):
    STORE[name].update(items)


def srem(name, *items):
    for item in items:
        STORE[name].remove(item)


def sinter(*names):
    result = STORE[names[0]]
    for name in names[1:]:
        result = result.intersection(STORE[name])
    return result


def sunion(*names):
    result = STORE[names[0]]
    for name in names[1:]:
        result = result.union(STORE[name])
    return result


def scount(name):
    return len(STORE[name])


def lcreate(name):
    STORE[name] = []


def lappend(name, *items):
    STORE[name].extend(items)


def hcreate(name):
    STORE[name] = {}


def hset(name, *items):
    for item in items:
        k, v = item.split(':')
        STORE[name][k] = v


def hpop(name, *items):
    for item in items:
        del STORE[name][item]


def hkeys(name):
    return STORE[name].keys()


def hvalues(name):
    return STORE[name].values()


def hget(name, *items):
    result = []
    for item in items:
        result.append(STORE[name][item])
    return result


lget = sget
lrem = srem
hcount = lcount = scount
