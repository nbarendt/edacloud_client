from unittest2 import TestCase
from edacloud_client.restoperation import RESTService, UnsupportedScheme
from mock import Mock, mocksignature
from test_utils import HttpTestServer, SimpleGETHTTPRequestHandler

API_BASE = 'api'
VERSION = 'v2010-06-28'
USER = 'nobody'

HOSTNAME = 'hostname.com'
PORT = 8080

    
class RESTOperationURLParsingTestCase(TestCase):
    def test_ServiceOperationWillRaiseExceptionOnUnsupportedScheme(self):
        service = RESTService(HOSTNAME, PORT, dict(username=USER))
        self.assertRaises( UnsupportedScheme, service.get, 'ftp://')

    def test_OperationWillParseHostnameAndPortFromURLWithoutExplicitPort(self):
        service = RESTService(HOSTNAME, PORT, dict(username=USER))
        op = service.get('http://{0}'.format(HOSTNAME))
        expected_netloc = '{0}:{1}'.format(HOSTNAME, 80)
        self.assertEqual(expected_netloc, op.netloc)

    def test_OperationWillParsePath(self):
        service = RESTService(HOSTNAME, PORT, dict(username=USER))
        expected_path = '/index'
        op = service.get('http://{0}{1}'.format(HOSTNAME, expected_path))
        self.assertEqual(expected_path, op.path)

    def test_OperationWillParseQueryString(self):
        service = RESTService(HOSTNAME, PORT, dict(username=USER))
        expected_qs = 'hello=world&goodbye=world'
        op = service.get('http://{0}/?{1}'.format(HOSTNAME, expected_qs))
        self.assertEqual(expected_qs, op.query)

class RESTOperationLiveServerTestCase(TestCase):
    def setUp(self):
        self.fake_server = HttpTestServer()
        self.fake_server.start()

    def tearDown(self):
        self.fake_server.stop()

    def test_OperationWillDoHTTPOperation(self):
        class TestHandler(SimpleGETHTTPRequestHandler):
            resp = 'HelloWorld!'
        self.fake_server.replace_request_handler_with(TestHandler)
        service = RESTService(self.fake_server.hostname, self.fake_server.port, dict(username=USER))
        op = service.get('http://{0}:{1}/'.format(service.hostname, service.port))
        op.execute()
        self.assertEqual(TestHandler.resp, op.response)
        
