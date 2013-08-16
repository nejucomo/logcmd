import unittest
import time

from logcmd.procstream import ProcStream
from logcmd.tests.savestringio import SaveStringIO


class TagStreamTests (unittest.TestCase):
    def test_write_and_close(self):
        f = SaveStringIO()
        faketime = lambda: time.gmtime(0)
        ps = ProcStream(f, 7, faketime)

        ps.info.write('Whee!\n')
        ps.out.write('foo')
        ps.err.write('bar\n')
        ps.out.write('quz\n')
        ps.err.write('oops')
        ps.info.write('done')

        expected = """\
1970-01-01T00:00:00+0000|7|I|Whee!
1970-01-01T00:00:00+0000|7|E|bar
1970-01-01T00:00:00+0000|7|O|fooquz
"""
        self.assertEqual(expected, f.getvalue())

        ps.close()

        expected += """\
1970-01-01T00:00:00+0000|7|I|done
1970-01-01T00:00:00+0000|7|E|oops
"""
        self.assertEqual(expected, f.getvalue())
