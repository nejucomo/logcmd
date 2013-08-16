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
1970-01-01T00:00:00+0000 0 * Launched with args: ['foo', 'bar']
"""
        self.assertEqual(expected, sio.getvalue())
        self.assertIsNone(pman.check_closed())
        self.assertEqual(expected, sio.getvalue())

        for f in pman.readables:
            pman.handle_read(f)

        expected += """\
1970-01-01T00:00:00+0000 0 - I am:
1970-01-01T00:00:00+0000 0 - the stdout stream.
1970-01-01T00:00:00+0000 0 ! Hello!
1970-01-01T00:00:00+0000 0 ! stderr reporting for duty.
"""
        self.assertEqual(expected, sio.getvalue())
        self.assertEqual(0, pman.check_closed())

        expected += """\
1970-01-01T00:00:00+0000 0 - blah
1970-01-01T00:00:00+0000 0 * Process exited with status: 0
1970-01-01T00:00:00+0000 0 * Wall clock time: 0.000
"""
        self.assertEqual(expected, sio.getvalue())
