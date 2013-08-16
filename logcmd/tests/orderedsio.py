from StringIO import StringIO


class OrderedStringIO (StringIO):
    """StringIO w/ comparison on instantiation order for test determinism."""

    _serial = 0

    def __init__(self, *a, **kw):
        StringIO.__init__(self, *a, **kw)
        self._myserial = OrderedStringIO._serial
        OrderedStringIO._serial += 1

    def __cmp__(self, other):
        return cmp(self._myserial, other._myserial)

    def __hash__(self):
        return hash(self._myserial)


def fake_select(rds, wds, eds):
    """Assuming rds are OrderedStringIO, the return is deterministic."""
    assert (wds, eds) == ([], [])
    return (sorted(rds), [], [])
