import time

from logcmd.tagstream import TagStream


class ProcStream (object):

    def __init__(self, outstream, pid, _gettime=time.gmtime):
        metatmpl = '%%(TIME)s|%d|%s|%%(LINE)s\n'

        self._info = TagStream(outstream, metatmpl % (pid, 'I'), _gettime)
        self.out = TagStream(outstream, metatmpl % (pid, 'O'), _gettime)
        self.err = TagStream(outstream, metatmpl % (pid, 'E'), _gettime)

    def info(self, tmpl, *args):
        self._info.write((tmpl % args) + '\n')

    def flush(self):
        for f in [self._info, self.out, self.err]:
            f.flush()

    def close(self):
        self.flush()
        self._info.close()
