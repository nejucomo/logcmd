import unittest
import time
from cStringIO import StringIO

from logcmd.iomanager import IOManager
from logcmd.tests.fakepopen import FakePopenFactory


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
        fakeselect = lambda rds, wds, eds: (rds, wds, eds)

        ioman = IOManager(sio, fakeselect, popen, faketime)
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
1970-01-01T00:00:00+0000 1 * Process exited due to signal: 7
"""
        # Because of mapping non-determinism, we sort the lines for comparison:
        sorted_lines = lambda s: sorted(s.split('\n'))
        self.assertEqual(sorted_lines(expected), sorted_lines(sio.getvalue()))
