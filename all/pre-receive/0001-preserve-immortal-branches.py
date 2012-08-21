#!/usr/bin/env python
import sys
import os.path

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import tools.git as git


def main(stdin, config, *args):
    conf_val = config.get('hooks.immortal-branches', '')
    immortal_branches = set(b.strip() for b in conf_val.split(',') if b.strip())
    immortal_refnames = set('refs/heads/%s' % b for b in immortal_branches)

    for line in stdin.readlines():
        oldrev, newrev, refname = line.split()
        if newrev == ('0' * 40) and refname in immortal_refnames:
            raise Exception('Can\'t delete immortal branch %r', refname)


if __name__ == '__main__':
    try:
        main(sys.stdin, git.config(), *sys.argv[1:])
    except Exception as e:
        sys.stderr.write((e.args[0] % e.args[1:]) + '\n')
        sys.exit(1)
