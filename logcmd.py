#! /usr/bin/env python

import os
import sys
import time
import urllib
import select
import subprocess


DESCRIPTION = """
Run a command logging and prettifying the output.
"""

LOG_DIR = os.path.expanduser('~/logs/logcmd')

ISO_8601 = '%Y-%m-%dT%H:%M:%S%z'


def main(args = sys.argv[1:]):
    timestart = time.time()
    log = Logger(args, timestart)

    proc = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    rd2stream = {
        proc.stdout: 'O',
        proc.stderr: 'E',
        }

    while (proc.returncode is None) or os.WIFSTOPPED(proc.returncode) or os.WIFCONTINUED(proc.returncode):
        while proc.poll() is None:
            (rds, wds, xds) = select.select([proc.stdout, proc.stderr], [], [])
            assert (wds, xds) == ([], []), `rds, wds, xds`
            for rd in rds:
                chunk = rd.readline()
                log(rd2stream[rd], '%s', chunk)

        assert proc.returncode is not None

        if os.WIFSTOPPED(proc.returncode):
            log('I', 'Process stopped with signal: %r\n', os.WSTOPSIG(proc.returncode))
        elif os.WIFCONTINUED(proc.returncode):
            log('I', 'Process continued. (status: %x)\n', proc.returncode)
        elif os.WIFSIGNALED(proc.returncode):
            log('I', 'Process exited due to signal: %r\n', os.WTERMSIG(proc.returncode))
        elif os.WIFEXITED(proc.returncode):
            log('I', 'Process exited with status: %r\n', os.WEXITSTATUS(proc.returncode))
        else:
            log('I', 'Error; unknown exit status: %r\n', proc.returncode)

    log('I', 'Wall-clock time: %r seconds.', time.time() - timestart)
    log.close()


class Logger (object):
    def __init__(self, args, timestart):
        date = time.strftime(ISO_8601, time.gmtime(timestart))
        cmdenc = '+'.join( urllib.quote(arg, '') for arg in args )
        stem = os.path.join(LOG_DIR, '%s.%s.' % (date, cmdenc))

        self._terminal = sys.stdout
        self._combined = file(stem + 'log', 'w')
        self._split = file(stem + 'streamlog', 'w')
        self._bufs = {
            'I': '',
            'O': '',
            'E': '',
            }
        self._decorations = {
            self._terminal: {
                'I': '\x1B[32m%s\x1B[0m',
                'O': '\x1B[0m%s',
                'E': '\x1B[33m%s\x1B[0m',
                },
            self._combined: {
                'I': '%s',
                'O': '%s',
                'E': '%s',
                },
            self._split: {
                'I': 'I:%s',
                'O': 'O:%s',
                'E': 'E:%s',
                },
            }

        self('I', 'Launching %r on %s.\n', args, date)

    def __call__(self, stream, tmpl, *args):
        buf = self._bufs[stream]
        buf += tmpl % args
        lines = buf.split('\n')
        self._bufs[stream] = lines.pop()

        for line in lines:
            self._write(stream, line)

    def close(self):
        for stream, buf in self._bufs.items():
            if buf:
                self._write(stream, buf)

        for f in (self._split, self._combined, self._terminal):
            f.close()

    def _write(self, stream, line):
        if stream == 'I':
            fs = (self._split, self._terminal)
        else:
            fs = (self._split, self._combined, self._terminal)

        for f in fs:
            decorations = self._decorations[f]
            decotmpl = decorations[stream]
            output = decotmpl % (line,)
            f.write(output + '\n')


if __name__ == '__main__':
    main()
