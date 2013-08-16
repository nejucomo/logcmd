import time

from logcmd.defaults import DefaultTemplate
from logcmd.tagstream import TagStream


class ProcStream (object):

    def __init__(self,
                 outstream,
                 pid,
                 tmpl=DefaultTemplate,
                 params=None,
                 _gettime=time.gmtime,
                 ):

        def make_stream(tag):
            return TagStream(
                outstream,
                tmpl,
                {'PID': pid,
                 'TAG': tag},
                _gettime=_gettime)

        self._info = make_stream('*')
        self.out = make_stream('-')
        self.err = make_stream('!')

    def info(self, tmpl, *args):
        self._info.write((tmpl % args) + '\n')

    def flush(self):
        for f in [self._info, self.out, self.err]:
            f.flush()

    def close(self):
        self.flush()
