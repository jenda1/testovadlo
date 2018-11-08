import json
import argparse
import sys
import pathlib
import re
import logging

logger = logging.getLogger(__package__)

path_arg = pathlib.Path("/data/arg")

def main():
    parser = argparse.ArgumentParser(prog="wiki_inputs", description="wiki_inputs helper")
    subparsers = parser.add_subparsers(dest="command", help='commands')

    parser.add_argument("-v", "--verbose", dest="verbose_count",
                        action="count", default=0,
                        help="increases log verbosity for each occurence.")

    get_parser = subparsers.add_parser('get')
    get_parser.add_argument("arg", type=int, help="# of argument")

    arguments = parser.parse_args()

    logger.setLevel(max(3 - arguments.verbose_count, 0) * 10)

    if arguments.command == 'get':
        try:
            get(arguments.arg)
        except:
            logger.exception("error")
            sys.exit(1)


def get(n):
    fn = path_arg/f"{n}.json"

    try:
        with open(fn, "r") as fh:
            val = json.load(fh)
    except:
        raise Exception(f"{n}: invalid argument")

    return val


hodnoceni_re = re.compile("\((?P<op>[+=-]?)(?P<num>\d+)\)")

def hodnoceni2procenta(n):
    val = get(n)

    if val['type'] not in ['text','textarea']:
        raise Exception(f"{n}: invalid type: {val['type']}")
    if val['val'] is None:
        return None

    out = 100

    for m in hodnoceni_re.finditer(val['val']):
        if m.group('op') in ['', '-']:
            out -= int(m.group('num'))
        elif m.group('op') == '=':
            out = int(m.group('num'))
        elif m.group('op') == '+':
            out += int(m.group('num'))

    if out < 0:
        out = 0
    if out > 100:
        out = 100

    return int(out)
