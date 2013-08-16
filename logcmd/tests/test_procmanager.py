import unittest
import time
import subprocess
from cStringIO import StringIO

from logcmd.procmanager import ProcManager
from logcmd.tests.savestringio import SaveStringIO


class TagStreamTests (unittest.TestCase):
    def test_write_and_close(self):
        ssio = SaveStringIO()
        args = ['foo', 'bar']
        faketime = lambda: time.gmtime(0)
        popen = lambda *a, **kw: FakePopen(self, args, *a, **kw)

        pman = ProcManager(ssio, args, _popen=popen, _gettime=faketime)

        expected = """\
1970-01-01T00:00:00+0000|7|I|Launched with args: ['foo', 'bar']
"""
        self.assertEqual(expected, ssio.getvalue())

        for f in pman.readables:
            pman.handle_read(f)

        expected += """\
1970-01-01T00:00:00+0000|7|O|I am:
1970-01-01T00:00:00+0000|7|O|the stdout stream.
1970-01-01T00:00:00+0000|7|E|Hello!
1970-01-01T00:00:00+0000|7|E|stderr reporting for duty.
"""
        self.assertEqual(expected, ssio.getvalue())


class FakePopen (object):
    def __init__(self, testcase, expectedargs, args, shell, stdout, stderr):
        self.pid = 7
        self.stdout = StringIO('I am:\nthe stdout stream.\n')
        self.stderr = StringIO('Hello!\nstderr reporting for duty.\n')

        self._tc = testcase
        self._tc.assertEqual(expectedargs, args)
        self._tc.assertFalse(shell)
        self._tc.assertEqual(subprocess.PIPE, stdout)
        self._tc.assertEqual(subprocess.PIPE, stderr)
