import sys
import os
from os.path import abspath, dirname, join


def amend_path(fname, tests_dir = 'tests'):
    '''
    when running 'project/unittests/module/test_foo.py', test_foo.py will usually
    want to import 'module.foo'. Calling amend_path(__file__) from test_foo.py will
    put 'project/module' in sys.path
    '''
    project_root, _unittests, src_path = abspath(dirname(fname)).partition(os.sep + tests_dir + os.sep)
    sys.path.append(join(project_root, src_path))
