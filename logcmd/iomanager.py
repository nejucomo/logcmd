import time
import subprocess
import select
from logcmd.procmanager import ProcManager


class IOManager (object):
    def __init__(self,
                 outstream,
                 _select=select.select,
                 _popen=subprocess.Popen,
                 _gettime=time.gmtime):

        self._outstream = outstream
        self._select = _select
        self._popen = _popen
        self._gettime = _gettime
        self._readables = {}
        self._pms = set()
        self._exitstatus = 0

    def launch(self, args):
        pman = ProcManager(self._outstream,
                           args,
                           _popen=self._popen,
                           _gettime=self._gettime)

        self._pms.add(pman)
        for f in pman.readables:
            self._readables[f] = pman

    def mainloop(self):
        while len(self._pms) > 0:
            self._filter_closed_processes()
            self._handle_io()
        return self._exitstatus

    def _filter_closed_processes(self):
        for pm in list(self._pms):
            rc = pm.check_closed()
            if rc is None:
                continue
            else:
                self._pms.remove(pm)
                for f in pm.readables:
                    del self._readables[f]
                if rc != 0:
                    self._exitstatus = 1

    def _handle_io(self):
        (rds, wds, xds) = self._select(self._readables.keys(), [], [])
        assert (wds, xds) == ([], []), repr((rds, wds, xds))

        for rd in rds:
            self._readables[rd].handle_read(rd)