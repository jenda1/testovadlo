import json
import argparse
import sys
import pathlib
import re
import logging
import base64
import os

logger = logging.getLogger(__package__)

path_arg = pathlib.Path("/arg")


def main():
    parser = argparse.ArgumentParser(prog="wiki_inputs", description="wiki_inputs helper")
    subparsers = parser.add_subparsers(dest="command", help='commands')

    parser.add_argument("-v", "--verbose", dest="verbose_count",
                        action="count", default=0,
                        help="increases log verbosity for each occurence.")

    get_parser = subparsers.add_parser('get', description="get argument or input value")
    get_parser.add_argument("--owner", required=False, help="owner name or _group name_ or _all_")
    get_parser.add_argument("arg", help="argument")

    get_parser = subparsers.add_parser('h2p', description="get argument or input value and transform hodnoceni to percents")
    get_parser.add_argument("--owner", required=False, help="owner name or _group name_ or _all_")
    get_parser.add_argument("arg", help="argument")

    arguments = parser.parse_args()
    logger.setLevel(max(3 - arguments.verbose_count, 0) * 10)

    out = None
    if arguments.command == 'get':
        out = get(arguments.arg, arguments.owner)
    elif arguments.command == 'h2p':
        out = h2p(arguments.arg, arguments.owner)

    if type(out) == list:
        print("\n".join(out))
    elif out is not None:
        print(str(out))


def get(name, owner=None):
    fn = str(name).replace("/", "_")
    if owner:
        try:
            owner = get(str(int(owner)))
        except ValueError:
            pass

        fn += "@" + str(owner)

    try:
        with open(path_arg/f"{fn}.json", "r") as fh:
            val = json.load(fh)
    except FileNotFoundError:
        if type(name) != int:
            print("#WI_NATIVE " + json.dumps({'type': 'getval',
                                              'val': str(name),
                                              'user': owner,
                                              'id': fn}),
                  file=sys.stderr)
        return

    if val['type'] is None:
        return None

    elif val['type'] in ["str", "int", "float"]:
        return val['val']

    elif val['type'] in ["file", "files"]:
        out = list()
        curr = os.path.realpath(os.getcwd())

        if val['val']:
            for fl in val['val']:
                d = os.path.realpath(os.path.join(curr, fl['name']))
                assert os.path.commonprefix([curr, d]) == curr

                with open(d, "wb") as fd:
                    out.append(d)
                    fd.write(base64.b64decode(fl['content']))

        return out

    else:
        return val['val']


hodnoceni_re = re.compile(r"\((?P<op>[+=-]?)(?P<num>\d+)\)")


def hodnoceni2procenta(name, owner=None):
    val = get(name, owner)

    if val is None:
        return None

    out = 100

    for m in hodnoceni_re.finditer(val):
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


def h2p(name, owner=None):
    return hodnoceni2procenta(name, owner)
