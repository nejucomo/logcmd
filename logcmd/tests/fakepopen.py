import subprocess

from logcmd.tests.orderedsio import OrderedStringIO


class FakePopenFactory (object):

    def __init__(self, testcase, *infos):
        self._tc = testcase
        self._infos = infos
        self._nextpid = 0

    def __call__(self, args, shell, stdout, stderr):

        pid = self._nextpid
        info = self._infos[pid]
        self._nextpid += 1

        self._tc.assertEqual(info['args'], args)
        self._tc.assertFalse(shell)
        self._tc.assertEqual(subprocess.PIPE, stdout)
        self._tc.assertEqual(subprocess.PIPE, stderr)

        return FakePopen(
            pid,
            info['status'],
            OrderedStringIO(info['out']),
            OrderedStringIO(info['err']))


class FakePopen (object):
    def __init__(self, pid, status, stdout, stderr):
        self.pid = pid
        self.stdout = stdout
        self.stderr = stderr
        self._status = status

    def poll(self):
        if self.stdout.tell() < len(self.stdout.getvalue()):
            return None
        elif self.stderr.tell() < len(self.stderr.getvalue()):
            return None
        else:
            return self._status
