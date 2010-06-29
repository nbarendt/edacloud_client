from httplib import HTTPConnection
import json
from urlparse import urlparse

class UnsupportedScheme(Exception):
    def __init__(self, unsupported_scheme):
        self.scheme = unsupported_scheme

    def __str__(self):
        return 'Unsupported Scheme: {0}'.format(self.scheme)
    
class RESTService(object):
    def __init__(self, hostname, port, credentials):
        self.hostname = hostname
        self.port = port
        self.credentials = credentials

    def get(self, url, data=None):
        return RESTOperation(self, 'GET', url, data)

DEFAULT_HTTP_PORT = '80'

class RESTOperation(object):
    def __init__(self, service, method, url, data=None):
        self.service = service
        self.method = method
        self.parse_url(url)
        self.data = data

    def parse_url(self, url):
        self.scheme, self.netloc, self.path, params, self.query, fragment = urlparse(url)
        if self.scheme != 'http':
            raise UnsupportedScheme(self.scheme)
        if ':' not in self.netloc:
            self.netloc = ':'.join([self.netloc, DEFAULT_HTTP_PORT])

    def execute(self):
        hostname, port = self.netloc.split(':', 1)
        conn = HTTPConnection(hostname, port)
        conn.request(self.method, self.path, self.data)
        self.result = conn.getresponse()

    @property
    def response(self):
        return self.result.read()



def make_request(method, url, data='', decodeJSONresult=False):
        (scheme, netloc, path, params, query, fragment) = urlparse(url)
        if scheme != 'http':
            raise Exception('Unsupported URL scheme: %s' % scheme)
        host, port = netloc.split(':', 1)
        conn = HTTPConnection(host, port)
        conn.request(method, path, data)
        result = conn.getresponse()
        if result.status not in [200,204]:
            raise Exception('%s on %s returned status of %s with response body of %s' % (method, url, result.status, result.read()))
        if decodeJSONresult:
            result = result.read()
            result = json.loads(result)
        return result
