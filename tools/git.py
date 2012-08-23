import sys
import re
import os
import util

import dulwich.repo
import dulwich.config
import dulwich.objects


def config():
    c = {}

    for line in util.run('git', 'config', '--list').stdout.splitlines():
        k, v = line.split('=', 1)
        c[k] = v

    return c

author_re = re.compile(r'^(?P<name>.+?)?(\s?)(?:<(?P<email>.+?)>)?$')


def author_username(author_str):
    email = author_email(author_str)
    if email is None or '@' not in email:
        return None
    return email.split('@')[0]


def author_email(author_str):
    return author_re.match(author_str).group('email')


def author_name(author_str):
    return author_re.match(author_str).group('name')


def hook_driver(func):
    '''
    Run a function as a git hook, forwarding stdin, a Repo object, and all command-line args
    to the function. If an exception is raised, exits with errorcode=1, indicating failure.
    '''
    try:
        func(sys.stdin, Repo(), *sys.argv[1:])
    except Exception as e:
        try:
            message = (e.args[0] % e.args[1])
        except Exception:
            message = str(e)
        sys.stderr.write(message + '\n')
        sys.exit(1)


def receive_refs(repo, stream):
    '''
    For pre- and post- receive hooks, stdin has a list of: old, new, refname
    This is a convenience wrapper to read from a stream and return those as objects.
    '''
    for line in stream.readlines():
        oldobj_id, newobj_id, refname = line.split(' ', 2)
        yield repo[oldobj_id], repo[newobj_id], refname


def null_object(thing):
    return thing.id == ('0' * 40)


class Config(dulwich.config.StackedConfig):
    _config_default = object()

    def __init__(self, stacked_config):
        super(Config, self).__init__(stacked_config.backends, stacked_config.writable)

    def get(self, key, default = _config_default):
        keyparts = key.split('.')
        name = keyparts[-1]
        section = tuple(keyparts[:-1])
        try:
            return super(Config, self).get(section, name)
        except KeyError:
            if default is  self._config_default:
                raise
            else:
                return default


class Repo(dulwich.repo.Repo):
    def __init__(self, pth = None):
        if pth is None:
            pth = os.environ.get('GIT_DIR')
        super(Repo, self).__init__(pth)

    @property
    def config(self):
        return Config(self.get_config_stack())
