import unittest
import time
from cStringIO import StringIO

from logcmd.procmanager import ProcManager
from logcmd.tests.fakepopen import FakePopenFactory


class ProcManagerTests (unittest.TestCase):
    def test_handle_read(self):
        sio = StringIO()
        args = ['foo', 'bar']
        faketime = lambda: time.gmtime(0)
        popen = FakePopenFactory(
            self,
            args,
            'I am:\nthe stdout stream.\n',
            'Hello!\nstderr reporting for duty.\n',
            )

        pman = ProcManager(sio, args, _popen=popen, _gettime=faketime)

        expected = """\
1970-01-01T00:00:00+0000|0|I|Launched with args: ['foo', 'bar']
"""
        self.assertEqual(expected, sio.getvalue())

        for f in pman.readables:
            pman.handle_read(f)

        expected += """\
1970-01-01T00:00:00+0000|0|O|I am:
1970-01-01T00:00:00+0000|0|O|the stdout stream.
1970-01-01T00:00:00+0000|0|E|Hello!
1970-01-01T00:00:00+0000|0|E|stderr reporting for duty.
"""
        self.assertEqual(expected, sio.getvalue())
