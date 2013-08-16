import time
import subprocess

from logcmd.procstream import ProcStream


class ProcManager (object):

    _BUFSIZE = 2**16

    @property
    def readables(self):
        return (self._proc.stdout, self._proc.stderr)

    def __init__(self,
                 outstream,
                 args,
                 _popen=subprocess.Popen,
                 _gettime=time.gmtime,
                 ):
        self._proc = _popen(
            args,
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        self._ps = ProcStream(outstream, self._proc.pid, _gettime=_gettime)

        self._writers = {
            self._proc.stdout: self._ps.out,
            self._proc.stderr: self._ps.err,
            }

        self._ps.info('Launched with args: %r', args)

    def handle_read(self, f):
        writer = self._writers[f]
        chunk = f.read(self._BUFSIZE)
        writer.write(chunk)
