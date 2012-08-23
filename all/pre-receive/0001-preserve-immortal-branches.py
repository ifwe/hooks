#!/usr/bin/env python
'''
A git pre-receive hook to deny deletion of any branch deemed immortal by
'hooks.immortal-branches'.

Configure as follows (in a bare repository):
    git config hooks.immortal-branches "master, very-important-branch"

If a branch is deleted and its name matches one of the values in this list,
the receive will be denied with an appropriate message to the pusher.
'''
import tools.git as git


def main(stdin, repo, *args):
    conf_val = repo.config.get('hooks.immortal-branches', '')
    immortal_refnames = set('refs/heads/%s' % b.strip() for b in conf_val.split(',') if b.strip())

    for old, new, refname in git.receive_refs(repo, stdin):
        if refname in immortal_refnames and git.null_object(new):
            raise Exception('Can\'t delete immortal branch %r', refname)


if __name__ == '__main__':
    git.hook_driver(main)
