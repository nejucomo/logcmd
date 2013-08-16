import unittest
import time
from cStringIO import StringIO

from logcmd.main import main
from logcmd.tests.fakepopen import FakePopenFactory


class MainTests (unittest.TestCase):

    def _run_main_and_verify(self, args, expectedout, status):
        sio = StringIO()
        fake_exit_calls = []
        fake_exit = fake_exit_calls.append
        fake_select = lambda rds, wds, eds: (rds, wds, eds)
        fake_popen = FakePopenFactory(
            self,
            dict(
                args=args,
                status=status,
                out='A\n',
                err='B\n',
                ),
            )
        fake_time = lambda: time.gmtime(0)

        main(
            args=args,
            _stdout=sio,
            _exit=fake_exit,
            _select=fake_select,
            _popen=fake_popen,
            _gettime=fake_time,
            )

        self.assertEqual(expectedout, sio.getvalue())
        self.assertEqual([status], fake_exit_calls)

    def test_default(self):
        self._run_main_and_verify(
            ['foo', 'bar'],
            status=0,
            expectedout="""\
1970-01-01T00:00:00+0000 0 * Launched with args: ['foo', 'bar']
1970-01-01T00:00:00+0000 0 - A
1970-01-01T00:00:00+0000 0 ! B
1970-01-01T00:00:00+0000 0 * Process exited with status: 0
1970-01-01T00:00:00+0000 0 * Wall clock time: 0.000
""",
            )

    def test_subcommand_parameter_collision(self):
        self._run_main_and_verify(
            ['foo', '-t', 'bar'],
            status=0,
            expectedout="""\
1970-01-01T00:00:00+0000 0 * Launched with args: ['foo', '-t', 'bar']
1970-01-01T00:00:00+0000 0 - A
1970-01-01T00:00:00+0000 0 ! B
1970-01-01T00:00:00+0000 0 * Process exited with status: 0
1970-01-01T00:00:00+0000 0 * Wall clock time: 0.000
""",
            )
