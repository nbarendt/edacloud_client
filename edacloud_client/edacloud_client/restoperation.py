from httplib import HTTPConnection
import json
from urlparse import urlparse

DEFAULT_HTTP_PORT = '80'

class UnsupportedScheme(Exception):
    def __init__(self, unsupported_scheme):
        self.scheme = unsupported_scheme

    def __str__(self):
        return 'Unsupported Scheme: {0}'.format(self.scheme)

class HTTPError(Exception):
    def __init__(self, status, reason):
        self.status = status
        self.reason = reason

    def __str__(self):
        return 'HTTP Server Returned {0} : {1}'.format(self.status, self.reason)

class RESTOperation(object):
    def __init__(self, service, method, url, data=''):
        self.service = service
        self.method = method
        self.parse_url(url)
        self.request_data = data
        self.encode_request = None
        self.decode_response = None

    def parse_url(self, url):
        self.scheme, self.netloc, self.path, params, self.query, fragment = urlparse(url)
        if self.scheme != 'http':
            raise UnsupportedScheme(self.scheme)
        if ':' not in self.netloc:
            self.netloc = ':'.join([self.netloc, DEFAULT_HTTP_PORT])

    def make_connection(self):
        hostname, port = self.netloc.split(':', 1)
        self.connection = HTTPConnection(hostname, port)

    def encode_request_data(self, data):
        return data
    
    def make_request(self):
        self.connection.request(self.method, self.path, self.encode_request_data(self.request_data))

    def get_response(self):
        self.result = self.connection.getresponse()
        if self.result.status not in [200, 204]:
            raise HTTPError(self.result.status, self.result.reason)
        self.response = self.decode_response_data(self.result.read())

    def decode_response_data(self, data):
        return data
    
    def execute(self):
        self.make_connection()
        self.make_request()
        self.get_response()

class JSONRESTOperation(RESTOperation):
    def encode_request_data(self, data):
        return json.dumps(data)

    def decode_response_data(self, data):
        return json.loads(data) if data else None

class RESTService(object):
    operation_class = RESTOperation
    def __init__(self, hostname, port, credentials):
        self.hostname = hostname
        self.port = port
        self.credentials = credentials

    def get(self, url, data=''):
        return self.operation_class(self, 'GET', url, data)

class JSONRESTService(RESTService):
    operation_class = JSONRESTOperation
