import urllib
import urllib2
import urlparse


class Jenkins(object):
    host = 'acceptbuild01.tag-dev.com'
    port = 8080
    params = dict(delay = '1sec')
    path = '/job/%(jobname)s/build'

    def __init__(self, jobname, host = None, port = None, params = None, path = None):
        if host is not None:
            self.host = host
        if port is not None:
            self.port = port
        if params is not None:
            self.params = params
        if path is not None:
            self.path = path

        self.jobname = jobname

    def build(self):
        url = urlparse.urlunparse((
            'http',
            '%s:%s' % (self.host, self.port),
            self.path % vars(self),
            None,
            urllib.urlencode(self.params),
            None
        ))
        self.request(url)

    def request(self, url):
        urllib2.urlopen(url)
