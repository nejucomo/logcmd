#! /usr/bin/env python

import os
import sys
import time
import select
import subprocess


DESCRIPTION = """
Read the stdout/stderr of a child command; prefix lines with "O:" or
"E:" respectively; print status information about the child with a line
prefix of "I:".
"""

def main(args = sys.argv[1:]):
    timestart = time.time()
    proc = Process(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    outbuffers = {
        sys.stdout: DrainBuffer(),
        proc.stdin: DrainBuffer(),
        }
    inbuffers = {
        sys.stdin: LineBuffer(outbuffers[proc.stdin]),
        proc.stdout: LineBuffer(LinePrefixer('O:', outbuffers[sys.stdout])),
        proc.stderr: LineBuffer(LinePrefixer('E:', outbuffers[sys.stdout])),
        }
    infolog = LinePrefixer('I:', outbuffers[sys.stdout])


    while proc.running or proc.stopped:
        (rds, wds, xds) = select.select(inbuffers.keys(), outbuffers.keys(), [], [])
        assert xds == [], `rds, wds, xds`
        for rd in rds:
            lbuf = inbuffers[rd]
            if not lbuf.consume_from(rd):
                del inbuffers[rd]
        for wd in wds:
            dbuf = outbuffers[wd]
            dbuf.drain_to(wd)

        if proc.returncode is not None:
            infolog.write(proc.describe_status())

    assert proc.returncode is None, 'Loop invariant failure: proc.returncode %r' % (proc.returncode,)
    infolog.write(proc.describe_status())

    infolog.write('Wall-clock time: %r seconds.' % (time.time() - timestart,))
    infolog.close()


class Process (subprocess.Popen):
    @property
    def running(self):
        return (self.returncode is None) or (not self.stdout.closed) or (not self.stderr.closed)

    @property
    def stopped(self):
        return (os.WIFSTOPPED(self.returncode) or os.WIFCONTINUED(self.returncode))

    def describe_status(self):
        if self.returncode is None:
            return 'Still running.'
        elif os.WIFSTOPPED(self.returncode):
            return 'Process stopped with signal: %r\n' % (os.WSTOPSIG(self.returncode),)
        elif os.WIFCONTINUED(self.returncode):
            return 'Process continued. (status: %x)\n' % (self.returncode,)
        elif os.WIFSIGNALED(self.returncode):
            return 'Process exited due to signal: %r\n' % (os.WTERMSIG(self.returncode),)
        elif os.WIFEXITED(self.returncode):
            return 'Process exited with status: %r\n' % (os.WEXITSTATUS(self.returncode),)
        else:
            return 'Error; unknown exit status: %r\n' % (self.returncode,)


class DrainBuffer (object):
    def __init__(self):
        self._buf = ''
        self._producers = set()

    def write(self, data):
        self._buf += data

    def drain_to(self, f):
        if self._buf is None:
            f.close()
        else:
            # BUG: Does f.write block until everything is written?
            f.write(self._buf)
            self._buf = ''

    def register_producer(self, producer):
        self._producers.add(producer)

    def remove_producer(self, producer):
        self._producers.remove(producer)
        if not self._producers:
            self._buf = None


class LineBuffer (object):
    def __init__(self, outstream):
        self._buf = ''
        self._outstream = outstream
        self._outstream.register_producer(self)

    def close(self):
        self._outstream.remove_producer(self)

    def consume_from(self, rd):
        lines = (self._buf + rd.readline()).split('\n')
        self._buf = lines.pop()
        self._outstream.writelines(lines)


class LineBuffer (object):
    def __init__(self, prefix, outstream):
        self._prefix = prefix
        self._outstream = outstream
        self._outstream.register_producer(self)

    def x1
        self._outstream.remove_producer(self)


if __name__ == '__main__':
    main()
