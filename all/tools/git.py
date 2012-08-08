import util


def config():
    c = {}

    for line in util.run('git', 'config', '--list').stdout.splitlines():
        k, v = line.split('=', 1)
        c[k] = v

    return c
