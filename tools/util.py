import os
import sys
from os.path import join, abspath
import contextlib
import subprocess


@contextlib.contextmanager
def cd(*dirs):
    old_dir = abspath(os.curdir)

    try:
        os.chdir(join(*dirs))
        yield
    finally:
        os.chdir(old_dir)


def _stdout(*a, **k):
    stream = k.pop('file', sys.stdout)
    end = k.pop('end', '\n')
    sep = k.pop('sep', ' ')
    print >>stream, (sep.join(a) + end),


def _subprocess(args):
    proc = subprocess.Popen(args, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    proc.wait()
    proc._stderr_file = proc.stderr
    proc.stderr = proc._stderr_file.read()
    proc._stdout_file = proc.stdout
    proc.stdout = proc._stdout_file.read()
    return proc


def run(*args, **kwds):
    expect_return_code = kwds.pop('expect_return_code', 0)
    _subproc = kwds.get('_subprocess', _subprocess)
    proc = _subproc(args)

    if expect_return_code is not None and proc.returncode != expect_return_code:
        raise subprocess.CalledProcessError(proc.returncode, args, output = proc.stderr)

    if kwds.get('verbose'):
        _stdout(proc.stdout, end = '', file = sys.stdout)
        _stdout(proc.stderr, end = '', file = sys.stderr)

    return proc
