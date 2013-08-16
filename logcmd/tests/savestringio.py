from StringIO import StringIO


class SaveStringIO (StringIO):
    def close(self):
        self._value = self.getvalue()
        StringIO.close(self)

    def getvalue(self):
        if hasattr(self, '_value'):
            return self._value
        else:
            return StringIO.getvalue(self)
