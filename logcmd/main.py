import sys
from logcmd.iomanager import IOManager


def main(args=sys.argv[1:]):
    ioman = IOManager(sys.stdout)
    ioman.launch(args)
    sys.exit(ioman.mainloop())
