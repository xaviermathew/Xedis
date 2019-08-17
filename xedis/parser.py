import csv
from cStringIO import StringIO
import inspect
import string

from xavium.planner import Planner
from xavium.commands import is_parallelizable
from xedis import commands

COMMANDS = {
    'keys': commands.keys,
    'rem': commands.rem,
    'flush': commands.flush,
    'info': commands.info,
    'help': commands.help,

    'screate': commands.screate,
    'sget': commands.sget,
    'sadd': commands.sadd,
    'srem': commands.srem,
    'sinter': commands.sinter,
    'sunion': commands.sunion,
    'scount': commands.scount,

    'lcreate': commands.lcreate,
    'lget': commands.lget,
    'lrem': commands.lrem,
    'lappend': commands.lappend,
    'lcount': commands.lcount,

    'hcreate': commands.hcreate,
    'hget': commands.hget,
    'hset': commands.hset,
    'hpop': commands.hpop,
    'hkeys': commands.hkeys,
    'hvalues': commands.hvalues,
    'hcount': commands.hcount,
}


class InvalidCommand(Exception):
    pass


def parse_delimited(s, delimiter):
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
        args = parse_delimited(arg_str, delimiter=' ')
    except StopIteration:
        return ()
    else:
        return map(typecast, args)


def parse_arg_set(fn, arg_str):
    sig = inspect.getargspec(fn)
    args = parse_args(arg_str)
    common_args = args[:len(sig.args) - 1]
    parallel_args = args[len(sig.args) - 1:]

    # in case fn is the first cmd in a pipe'd cmd list, parallel_args will be present
    #
    # for intermediary steps, only common_args will be populated; parallel_args will
    # be populated by xvm
    return common_args, parallel_args


def parse_fn(fn_str):
    try:
        return COMMANDS[fn_str]
    except KeyError:
        raise InvalidCommand('invalid command: %s' % fn_str)


def parse_fn_with_args(fn_str, arg_str):
    fn = parse_fn(fn_str)
    if is_parallelizable(fn):
        common_args, parallel_args = parse_arg_set(fn, arg_str)
        return fn, common_args, parallel_args
    else:
        args = parse_args(arg_str)
        return fn, args, []


def parse_line(line):
    cmd_list = parse_delimited(line, delimiter='|')
    parsed = []
    for cmd in cmd_list:
        try:
            fn_str, arg_str = cmd.split(' ', 1)
        except ValueError:
            fn = parse_fn(cmd)
            parsed.append((fn, [], []))
        else:
            fn, common_args, parallel_args = parse_fn_with_args(fn_str, arg_str)
            parsed.append((fn, common_args, parallel_args))
    return parsed


def parse(line):
    steps = parse_line(line)
    xvm = Planner(steps)
    return xvm.execute()
