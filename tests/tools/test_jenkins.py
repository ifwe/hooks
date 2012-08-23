import tests.helper as test_helper
test_helper.amend_path(__file__)

import unittest

import jenkins


class TestJenkins(unittest.TestCase):
    def test_url_build(self):
        jobname = 'foo'
        url = 'http://%(host)s:%(port)s%(path)s?delay=1sec' % (vars(jenkins.Jenkins))
        args_kwargs = []

        def mock_request(*args, **kwargs):
            args_kwargs[:] = [args, kwargs]

        j = jenkins.Jenkins(jobname)
        j.request = mock_request
        j.build()

        self.assertEqual(args_kwargs, [(url % dict(jobname=jobname),), {}])

    def test_build_jobs(self):
        old_build = jenkins.Jenkins.build

        build_calls = []

        def mock_build(self):
            build_calls.append(self)

        jenkins.Jenkins.build = mock_build

        job_lists = {
            None:   [],
            '':     [],
            ',':    [],
            'foo,': ['foo'],
            'foo,bar' : ['foo', 'bar'],
            'foo, bar' : ['foo', 'bar'],
            ',foo' : ['foo'],
        }

        for job_list, built_jobs in job_lists.items():
            build_calls[:] = []
            jenkins.build_jobs(job_list)
            self.assertEqual(tuple(x.jobname for x in build_calls), tuple(built_jobs))

        jenkins.Jenkins.build = old_build
