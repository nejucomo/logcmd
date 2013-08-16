import os
import time
import subprocess

from logcmd.defaults import DefaultTemplate
from logcmd.procstream import ProcStream


class ProcManager (object):

    _BUFSIZE = 2**16

    @property
    def readables(self):
        return (self._proc.stdout, self._proc.stderr)

    def __init__(self,
                 outstream,
                 args,
                 tmpl=DefaultTemplate,
                 params=None,
                 _popen=subprocess.Popen,
                 _gettime=time.gmtime,
                 ):

        self._gettime = _gettime
        self._starttime = time.mktime(_gettime())

        self._proc = _popen(
            args,
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        self._ps = ProcStream(
            outstream,
            self._proc.pid,
            tmpl,
            params,
            _gettime=_gettime)

        self._writers = {
            self._proc.stdout: self._ps.out,
            self._proc.stderr: self._ps.err,
            }

        self._ps.info('Launched with args: %r', args)

    def handle_read(self, f):
        writer = self._writers[f]
        chunk = f.read(self._BUFSIZE)
        if len(chunk) > 0:
            writer.write(chunk)
            return True
        else:
            return False

    def check_closed(self):
        rc = self._proc.poll()

        if rc is None:
            return None

        self._ps.flush()

        if os.WIFSTOPPED(rc):
            self._ps.info('Process stopped with signal: %r',
                          os.WSTOPSIG(rc))

        elif os.WIFCONTINUED(rc):
            self._ps.info('Process continued. (status: %x)',
                          rc)

        elif os.WIFSIGNALED(rc):
            self._ps.info('Process exited due to signal: %r',
                          os.WTERMSIG(rc))

        elif os.WIFEXITED(rc):
            self._ps.info('Process exited with status: %r',
                          os.WEXITSTATUS(rc))

        else:
            self._ps.info('Error; unknown exit status: %r',
                          rc)

        endtime = time.mktime(self._gettime())
        self._ps.info('Wall clock time: %.3f', endtime - self._starttime)

        self._ps.close()
        return rc
