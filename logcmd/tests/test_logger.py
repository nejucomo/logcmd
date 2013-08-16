import os
import errno
import unittest
import shutil
from cStringIO import StringIO

from logcmd.logger import Logger


class LoggerTests (unittest.TestCase):
    def setUp(self):
        self._dir = '_unittest_data'
        try:
            shutil.rmtree(self._dir)
        except os.error, e:
            if e.errno != errno.ENOENT:
                raise
        else:
            print '\nRemoved: %r' % (self._dir,)

        os.mkdir(self._dir)

    def test_basic_operation(self):
        args = ['foo', 'bar']
        timestart = 0
        fakeout = StringIO()

        log = Logger(args, timestart, self._dir, fakeout)

        stem = '1970-01-01T00:00:00+0000.foo+bar.'
        combined = stem + 'log'
        streamlog = stem + 'streamlog'
        expected = [combined, streamlog]
        self.assertEqual(expected, sorted(os.listdir(self._dir)))

        log('I', 'infotest\n')
        log('E', 'no newline')
        log('O', 'outtest: %d\n', 7)

        log.close()

        with file(os.path.join(self._dir, combined)) as f:
            self.assertEqual('outtest: 7\nno newline\n', f.read())

        with file(os.path.join(self._dir, streamlog)) as f:
            expected = """\
I:Launching ['foo', 'bar'] on 1970-01-01T00:00:00+0000
I:infotest
O:outtest: 7
E:no newline
"""
            self.assertEqual(expected, f.read())
