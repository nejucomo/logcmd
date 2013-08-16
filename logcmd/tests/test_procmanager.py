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
            dict(
                args=args,
                status=0,
                out='I am:\nthe stdout stream.\nblah',
                err='Hello!\nstderr reporting for duty.\n',
                ),
            )

        pman = ProcManager(sio, args, _popen=popen, _gettime=faketime)

        expected = """\
1970-01-01T00:00:00+0000|0|I|Launched with args: ['foo', 'bar']
"""
        self.assertEqual(expected, sio.getvalue())
        self.assertIsNone(pman.check_closed())
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
        self.assertEqual(0, pman.check_closed())

        expected += """\
1970-01-01T00:00:00+0000|0|O|blah
1970-01-01T00:00:00+0000|0|I|Process exited with status: 0
"""
        self.assertEqual(expected, sio.getvalue())
