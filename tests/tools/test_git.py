import tests.helper as test_helper
test_helper.amend_path(__file__)

import unittest

import git


class TestGit(unittest.TestCase):
    def test_config(self):
        import util
        _old_run = util.run

        def mock_run(*args):
            print args
            if args == ('git', 'config', '--list'):
                return _old_run('echo', 'user.name=foo\nuser.email=foo@example.com')
            else:
                return _old_run(*args)

        util.run = mock_run
        config = git.config()
        self.assertEqual(config.get('user.name'), 'foo')
        self.assertEqual(config.get('user.email'), 'foo@example.com')

        util.run = _old_run
