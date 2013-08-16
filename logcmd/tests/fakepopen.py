import subprocess
from cStringIO import StringIO


class FakePopenFactory (object):

    def __init__(self, testcase, expectedargs, outdata, errdata):
        self._tc = testcase
        self._expectedargs = expectedargs
        self._outdata = outdata
        self._errdata = errdata
        self._nextpid = 0

    def __call__(self, args, shell, stdout, stderr):
        self._tc.assertEqual(self._expectedargs, args)
        self._tc.assertFalse(shell)
        self._tc.assertEqual(subprocess.PIPE, stdout)
        self._tc.assertEqual(subprocess.PIPE, stderr)

        pid = self._nextpid
        self._nextpid += 1

        return FakePopen(pid, StringIO(self._outdata), StringIO(self._errdata))


class FakePopen (object):
    def __init__(self, pid, stdout, stderr):
        self.pid = pid
        self.stdout = stdout
        self.stderr = stderr
