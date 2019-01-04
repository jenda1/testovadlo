import json
import argparse
import sys
import pathlib
import re
import logging
import base64
import os

logger = logging.getLogger(__package__)

PATH_ARG = pathlib.Path("/arg")


def main():
    parser = argparse.ArgumentParser(prog="wiki_inputs", description="wiki_inputs helper")
    subparsers = parser.add_subparsers(dest="command", help='commands')

    parser.add_argument("-v", "--verbose", dest="verbose_count",
                        action="count", default=0,
                        help="increases log verbosity for each occurence.")

    get_parser = subparsers.add_parser('get', description="get argument or input value")
    get_parser.add_argument("--owner", required=False, help="owner name or _group name_ or _all_")
    get_parser.add_argument("arg", help="argument")
    get_parser.add_argument("attr", nargs="*", help="attribute of the argument")

    get_parser = subparsers.add_parser('h2p', description="get argument or input value and transform hodnoceni to percents")
    get_parser.add_argument("--owner", required=False, help="owner name or _group name_ or _all_")
    get_parser.add_argument("arg", help="argument")

    get_parser = subparsers.add_parser('clear', description="clear the wikilt output buffer")

    get_parser = subparsers.add_parser('progress', description="display progress bar")
    get_parser.add_argument("val", type=int, default=50, nargs='?', help="percentage")

    arguments = parser.parse_args()
    logger.setLevel(max(3 - arguments.verbose_count, 0) * 10)

    out = None
    if arguments.command == 'get':
        out = get(arguments.arg, arguments.owner, arguments.attr)
    elif arguments.command == 'h2p':
        out = h2p(arguments.arg, arguments.owner)
    elif arguments.command == 'clear':
        out = "#WI_NATIVE clear"
    elif arguments.command == 'progress':
        out = f"#WI_NATIVE progress {arguments.val}"

    if type(out) == list:
        print("\n".join([str(x) for x in out]), flush=True)
    elif out is not None:
        print(str(out), flush=True)


def expand_files(val, fprefix=None):
    out = list()
    curr = os.path.realpath(os.getcwd())

    if fprefix:
        curr = os.path.join(curr, fprefix)

    if not val:
        return out

    for fl in val:
        d = os.path.realpath(os.path.join(curr, fl['name']))
        assert os.path.commonprefix([curr, d]) == curr

        pathlib.Path(d).parent.mkdir(parents=True, exist_ok=True)

        with open(d, "wb") as fd:
            out.append(d)
            fd.write(base64.b64decode(fl['content']))

    return out


def expand_val(val, fprefix=None):
    if type(val) is dict:
        if val.get('type') in ["file", "files"]:
            return expand_files(val['val'], fprefix)

        elif val.get('type') in ['user-list']:
            return [x for u, v in val['val'].items() for x in expand_val(v, str(u))]

    return val


def get(name, owner=None, attr=None):
    fn = str(name).replace("/", "_")
    if owner:
        try:
            owner = get(str(int(owner)))
        except ValueError:
            pass

        fn += "@" + str(owner)

    try:
        with open(PATH_ARG/f"{fn}.json", "r") as fh:
            val = json.load(fh)
    except FileNotFoundError:
        if type(name) != int:
            print("#WI_NATIVE " + json.dumps({'type': 'getval',
                                              'val': str(name),
                                              'user': owner,
                                              'id': fn}),
                  file=sys.stderr)
        return

    for a in attr:
        if a == '.':
            if type(val) is dict:
                return [k for k in val.keys()]
            elif type(val) is list:
                return [k for k in range(len(val))]
            else:
                return type(val)

        if type(val) is dict:
            val = val.get(a)
        elif type(val) is list:
            try:
                val = val[int(a)]
            except Exception:
                val = None
        else:
            val = None

    return expand_val(val)




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
