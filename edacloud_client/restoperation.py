from httplib import HTTPConnection
import json
from urlparse import urlparse
from edacloud_client.exceptions import UnsupportedURLScheme, HTTPError

DEFAULT_HTTP_PORT = '80'

class RESTOperation(object):
    def __init__(self, method, url, data='', headers={}):
        self.method = method
        self.parse_url(url)
        self.request_data = data
        self.encode_request = None
        self.decode_response = None
        self.headers = headers

    def parse_url(self, url):
        self.scheme, self.netloc, self.path, params, self.query, fragment =\
            urlparse(url)
        if self.scheme != 'http':
            raise UnsupportedURLScheme(self.scheme)
        if ':' not in self.netloc:
            self.netloc = ':'.join([self.netloc, DEFAULT_HTTP_PORT])

    def make_connection(self):
        hostname, port = self.netloc.split(':', 1)
        self.connection = HTTPConnection(hostname, port)

    def encode_request_data(self, data):
        return data
    
    def make_request(self):
        encoded_data = self.encode_request_data(self.request_data)
        self.connection.request(self.method, self.path, encoded_data,
            self.headers)

    def get_response(self):
        self.result = self.connection.getresponse()
        if self.result.status not in [200, 204]:
            raise HTTPError(self.result.status, self.result.reason)
        self.response = self.decode_response_data(self.result.read())

    def decode_response_data(self, data):
        return data

    def prepare_for_request(self):
        pass
    
    def execute(self):
        self.make_connection()
        self.prepare_for_request()
        self.make_request()
        self.get_response()

class JSONRESTOperation(RESTOperation):
    def encode_request_data(self, data):
        return json.dumps(data)

    def decode_response_data(self, data):
        return json.loads(data) if data else None

