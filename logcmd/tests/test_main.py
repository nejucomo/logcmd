import unittest
import time
from cStringIO import StringIO

from logcmd.main import main
from logcmd.tests.fakepopen import FakePopenFactory


class MainTests (unittest.TestCase):
    def test_default(self):
        sio = StringIO()
        fake_exit_calls = []
        fake_exit = fake_exit_calls.append
        fake_select = lambda rds, wds, eds: (rds, wds, eds)
        fake_popen = FakePopenFactory(
            self,
            dict(
                args=['foo', 'bar'],
                status=0,
                out='A\n',
                err='B\n',
                ),
            )
        fake_time = lambda: time.gmtime(0)

        main(
            args=['foo', 'bar'],
            _stdout=sio,
            _exit=fake_exit,
            _select=fake_select,
            _popen=fake_popen,
            _gettime=fake_time,
            )

        expected = """\
1970-01-01T00:00:00+0000 0 * Launched with args: ['foo', 'bar']
1970-01-01T00:00:00+0000 0 - A
1970-01-01T00:00:00+0000 0 ! B
1970-01-01T00:00:00+0000 0 * Process exited with status: 0
1970-01-01T00:00:00+0000 0 * Wall clock time: 0.000
"""
        self.assertEqual(expected, sio.getvalue())
        self.assertEqual([0], fake_exit_calls)
