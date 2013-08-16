import os
import sys
import time
import urllib


LOG_DIR = os.path.expanduser('~/logs/logcmd')

ISO_8601 = '%Y-%m-%dT%H:%M:%S%z'


class Logger (object):
    def __init__(self, args, timestart, logdir=LOG_DIR, stdout=sys.stdout):
        date = time.strftime(ISO_8601, time.gmtime(timestart))
        cmdenc = '+'.join(urllib.quote(arg, '') for arg in args)
        stem = os.path.join(logdir, '%s.%s.' % (date, cmdenc))

        self._terminal = stdout
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

        self('I', 'Launching %r on %s\n', args, date)

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
