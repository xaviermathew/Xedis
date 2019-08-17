from gc import get_referents
import inspect
import json
import sys
from types import ModuleType, FunctionType

from xavium.commands import is_parallelizable


# Custom objects know their class.
# Function objects seem to know way too much, including modules.
# Exclude modules as well.
BLACKLIST = type, ModuleType, FunctionType


def get_size(obj):
    # taken from https://stackoverflow.com/a/30316760
    """sum size of object & members."""
    if isinstance(obj, BLACKLIST):
        raise TypeError('get_size() does not take argument of type: '+ str(type(obj)))
    seen_ids = set()
    size = 0
    objects = [obj]
    while objects:
        need_referents = []
        for obj in objects:
            if not isinstance(obj, BLACKLIST) and id(obj) not in seen_ids:
                seen_ids.add(id(obj))
                size += sys.getsizeof(obj)
                need_referents.append(obj)
        objects = get_referents(*need_referents)
    return size


def get_signature(cmd):
    from xedis.parser import parse_fn
    fn = parse_fn(cmd)
    sig = inspect.getargspec(fn)
    syntax = [cmd]
    if sig.args:
        syntax.extend(sig.args)
    if sig.varargs:
        syntax.append('*%s' % sig.varargs)
    if is_parallelizable(fn) and syntax[-1] != cmd and not syntax[-1].startswith('*'):
        syntax[-1] = '*%s' % syntax[-1]
    return ' '.join(syntax)


class XedisEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        elif isinstance(obj, Exception):
            return repr(obj)
        else:
            return json.JSONEncoder.default(self, obj)


def serialize(data_or_ex):
    if isinstance(data_or_ex, Exception):
        payload = {'status': 500, 'error': data_or_ex}
    else:
        payload = {'status': 200, 'data': data_or_ex}
    return json.dumps(payload, cls=XedisEncoder)


def deserialize(json_str):
    return json.loads(json_str)
