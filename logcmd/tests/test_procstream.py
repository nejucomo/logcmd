import unittest
import time
from cStringIO import StringIO

from logcmd.procstream import ProcStream


class ProcStreamTests (unittest.TestCase):
    def test_write_and_close(self):
        f = StringIO()
        faketime = lambda: time.gmtime(0)
        ps = ProcStream(f, 7, _gettime=faketime)

        ps.info('Whee%s', '!')
        ps.out.write('foo')
        ps.err.write('bar\n')
        ps.out.write('quz\n')
        ps.err.write('oops')
        ps.info('done')

        expected = """\
1970-01-01T00:00:00+0000 7 * Whee!
1970-01-01T00:00:00+0000 7 ! bar
1970-01-01T00:00:00+0000 7 - fooquz
1970-01-01T00:00:00+0000 7 * done
"""
        self.assertEqual(expected, f.getvalue())

        ps.close()

        expected += """\
1970-01-01T00:00:00+0000 7 ! oops
"""
        self.assertEqual(expected, f.getvalue())
