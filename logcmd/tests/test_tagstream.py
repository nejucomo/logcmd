import unittest
import time
from StringIO import StringIO

from logcmd.tagstream import TagStream


class TagStreamTests (unittest.TestCase):
    def test_write_and_close(self):
        f = SaveStringIO()
        faketime = lambda: time.gmtime(0)
        ts = TagStream(f, '%(TIME)s|T|%(LINE)s\n', faketime)

        ts.write('fo')
        ts.write('o\nbar\n')
        ts.write('quz')

        expected = """\
1970-01-01T00:00:00+0000|T|foo
1970-01-01T00:00:00+0000|T|bar
"""
        self.assertEqual(expected, f.getvalue())

        ts.close()

        expected += '1970-01-01T00:00:00+0000|T|quz\n'
        self.assertEqual(expected, f.getvalue())


class SaveStringIO (StringIO):
    def close(self):
        self._value = self.getvalue()
        StringIO.close(self)

    def getvalue(self):
        if hasattr(self, '_value'):
            return self._value
        else:
            return StringIO.getvalue(self)
