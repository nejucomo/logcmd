import sys
import argparse
import select
import subprocess
import time
from logcmd.defaults import DefaultTemplate
from logcmd.iomanager import IOManager


DESCRIPTION = """
Log command stdout, stderr, arguments, exit status, and timings.
"""


def main(args=sys.argv[1:],
         _stdout=sys.stdout,
         _exit=sys.exit,
         _select=select.select,
         _popen=subprocess.Popen,
         _gettime=time.gmtime,
         ):

    opts = parse_args(args)
    ioman = IOManager(
        _stdout,
        tmpl=opts.TMPL,
        _select=_select,
        _popen=_popen,
        _gettime=_gettime,
        )
    subargs = [opts.COMMAND] + opts.ARG
    ioman.launch(subargs)
    _exit(ioman.mainloop())


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
