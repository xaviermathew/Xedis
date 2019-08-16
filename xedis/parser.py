import csv
from cStringIO import StringIO
import string

from xedis import commands

COMMANDS = {
    'keys': {'fn': commands.keys},
    'rem': {'fn': commands.rem},
    'flush': {'fn': commands.flush},
    'info': {'fn': commands.info},
    'help': {'fn': commands.help},

    'screate': {'fn': commands.screate},
    'sget': {'fn': commands.sget},
    'sadd': {'fn': commands.sadd},
    'srem': {'fn': commands.srem},
    'sinter': {'fn': commands.sinter},
    'sunion': {'fn': commands.sunion},
    'scount': {'fn': commands.scount},

    'lcreate': {'fn': commands.lcreate},
    'lget': {'fn': commands.lget},
    'lrem': {'fn': commands.lrem},
    'lappend': {'fn': commands.lappend},
    'lcount': {'fn': commands.lcount},

    'hcreate': {'fn': commands.hcreate},
    'hget': {'fn': commands.hget},
    'hset': {'fn': commands.hset},
    'hpop': {'fn': commands.hpop},
    'hkeys': {'fn': commands.hkeys},
    'hvalues': {'fn': commands.hvalues},
    'hcount': {'fn': commands.hcount},
}


class InvalidCommand(Exception):
    pass


def _parse_delimited(s, delimiter):
    parsed = next(csv.reader(StringIO(s), delimiter=delimiter))
    return map(string.strip, parsed)


def typecast(item):
    try:
        return int(item)
    except ValueError:
        try:
            return float(item)
        except ValueError:
            return item


def parse_args(arg_str):
    try:
        args = _parse_delimited(arg_str, delimiter=' ')
    except StopIteration:
        return ()
    else:
        return map(typecast, args)


def parse_fn(fn):
    try:
        return COMMANDS[fn]['fn']
    except KeyError:
        raise InvalidCommand('invalid command: %s' % fn)


def parse_line(line):
    cmd_list = _parse_delimited(line, delimiter='|')
    parsed = []
    for cmd in cmd_list:
        try:
            fn_str, arg_str = cmd.split(' ', 1)
        except ValueError:
            fn = parse_fn(cmd)
            parsed.append((fn, []))
        else:
            fn = parse_fn(fn_str)
            args = parse_args(arg_str)
            parsed.append((fn, args))
    return parsed


def parse(line):
    parsed = parse_line(line)
    fn, args = parsed[0]
    result = fn(*args)
    for fn, args in parsed[1:]:
        if isinstance(result, (list, set)):
            args.extend(result)
        else:
            args.append(result)
        result = fn(*args)
    return result
