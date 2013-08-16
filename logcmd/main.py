import sys
import argparse
from logcmd.defaults import DefaultTemplate
from logcmd.iomanager import IOManager


DESCRIPTION = """
Log command stdout, stderr, arguments, exit status, and timings.
"""


def main(args=sys.argv[1:]):
    opts = parse_args(args)
    ioman = IOManager(sys.stdout, tmpl=opts.TMPL)
    subargs = [opts.COMMAND] + opts.ARG
    ioman.launch(subargs)
    sys.exit(ioman.mainloop())


def parse_args(args):
    p = argparse.ArgumentParser(description=DESCRIPTION)

    p.add_argument('-t', '--tmpl', '--template',
                   dest='TMPL',
                   type=str,
                   default=DefaultTemplate,
                   help='The template for output lines.')

    p.add_argument('COMMAND',
                   type=str,
                   help='Subcommand to run.')

    p.add_argument('ARG',
                   type=str,
                   nargs='*',
                   help='Subcommand arguments.')

    return p.parse_args(args)
