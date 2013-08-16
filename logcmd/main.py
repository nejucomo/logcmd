import os
import sys
import time
import select
import subprocess

from logcmd.logger import Logger


def main(args = sys.argv[1:]):
    timestart = time.time()
    log = Logger(args, timestart)

    proc = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    rd2stream = {
        proc.stdout: 'O',
        proc.stderr: 'E',
        }

    while (proc.returncode is None) or os.WIFSTOPPED(proc.returncode) or os.WIFCONTINUED(proc.returncode):
        while proc.poll() is None:
            (rds, wds, xds) = select.select([proc.stdout, proc.stderr], [], [])
            assert (wds, xds) == ([], []), `rds, wds, xds`
            for rd in rds:
                chunk = rd.readline()
                log(rd2stream[rd], '%s', chunk)

        assert proc.returncode is not None

        if os.WIFSTOPPED(proc.returncode):
            log('I', 'Process stopped with signal: %r\n', os.WSTOPSIG(proc.returncode))
        elif os.WIFCONTINUED(proc.returncode):
            log('I', 'Process continued. (status: %x)\n', proc.returncode)
        elif os.WIFSIGNALED(proc.returncode):
            log('I', 'Process exited due to signal: %r\n', os.WTERMSIG(proc.returncode))
        elif os.WIFEXITED(proc.returncode):
            log('I', 'Process exited with status: %r\n', os.WEXITSTATUS(proc.returncode))
        else:
            log('I', 'Error; unknown exit status: %r\n', proc.returncode)

    log('I', 'Wall-clock time: %r seconds.', time.time() - timestart)
    log.close()
