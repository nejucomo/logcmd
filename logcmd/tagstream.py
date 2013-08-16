import time

ISO_8601 = '%Y-%m-%dT%H:%M:%S%z'


class TagStream (object):

    def __init__(self, outstream, tmpl, _gettime=time.gmtime):
        self._f = outstream
        self._tmpl = tmpl
        self._gettime = _gettime
        self._buf = ''

    def write(self, output):
        lines = (self._buf + output).split('\n')
        self._buf = lines.pop()

        for line in lines:
            self._write(line)

    def flush(self):
        if self._buf:
            self._write(self._buf)
            self._buf = ''

    def close(self):
        self.flush()
        self._f.close()

    def _write(self, line):
        self._f.write(
            self._tmpl % {
                'TIME': time.strftime(ISO_8601, self._gettime()),
                'LINE': line,
                })
