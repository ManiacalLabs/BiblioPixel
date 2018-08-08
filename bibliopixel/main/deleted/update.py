"""
Update BiblioPixel's dependencies
"""

import os, sys, subprocess
from ... util import log


def run(args):
    root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    code = 0

    with open(os.path.join(root, 'requirements.txt')) as f:
        for requirement in f.read().splitlines():
            process = subprocess.Popen(
                ['pip', 'install', requirement, '--upgrade'],
                stdout=subprocess.PIPE)
            output, err = process.communicate()
            exit_code = process.wait()
            if exit_code:
                log.printer('ERROR upgrading', requirement, output, err)
                code = exit_code
            else:
                log.printer('Upgraded', requirement)

    sys.exit(code)


def set_parser(parser):
    parser.set_defaults(run=run)
