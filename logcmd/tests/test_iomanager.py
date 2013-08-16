import unittest
import time
from cStringIO import StringIO

from logcmd.iomanager import IOManager
from logcmd.tests.fakepopen import FakePopenFactory
from logcmd.tests.orderedsio import fake_select


class ProcManagerTests (unittest.TestCase):
    def test_basic_operation(self):
        sio = StringIO()
        faketime = lambda: time.gmtime(0)
        popen = FakePopenFactory(
            self,
            dict(
                args=['foo', 'foofy'],
                status=0,
                out='A\n',
                err='B\n',
                ),
            dict(
                args=['bar', 'barfy'],
                status=0x107,
                out='C\n',
                err='D\n',
                ),
            )

        ioman = IOManager(
            sio,
            _select=fake_select,
            _popen=popen,
            _gettime=faketime,
            )

        ioman.launch(['foo', 'foofy'])
        ioman.launch(['bar', 'barfy'])
        status = ioman.mainloop()

        self.assertEqual(1, status)

        expected = """\
1970-01-01T00:00:00+0000 0 * Launched with args: ['foo', 'foofy']
1970-01-01T00:00:00+0000 1 * Launched with args: ['bar', 'barfy']
1970-01-01T00:00:00+0000 0 - A
1970-01-01T00:00:00+0000 0 ! B
1970-01-01T00:00:00+0000 1 - C
1970-01-01T00:00:00+0000 1 ! D
1970-01-01T00:00:00+0000 0 * Process exited with status: 0
1970-01-01T00:00:00+0000 0 * Wall clock time: 0.000
1970-01-01T00:00:00+0000 1 * Process exited due to signal: 7
1970-01-01T00:00:00+0000 1 * Wall clock time: 0.000
"""
        self.assertEqual(expected, sio.getvalue())
