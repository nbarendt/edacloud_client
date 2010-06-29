from unittest2 import TestCase
from edacloud_client.restoperation import RESTService, UnsupportedScheme, HTTPError
from mock import Mock, patch
from test_utils import HttpTestServer, SimpleGETHTTPRequestHandler
import edacloud_client.restoperation

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

class RESTOperationHTTPBehaviorTestCase(TestCase):
    def setUp(self):
        self.original = edacloud_client.restoperation.HTTPConnection
        self.mock_HTTPConnection = Mock(spec=self.original)
        edacloud_client.restoperation.HTTPConnection = self.mock_HTTPConnection
        self.service = RESTService(HOSTNAME, PORT, dict(username=USER))
        
    def tearDown(self):
        edacloud_client.restoperation.HTTPConnection = self.original

    def force_http_status(self, status, reason, response=''):
        request_mock = self.mock_HTTPConnection()
        request_mock.getresponse.return_value = Mock()
        request_mock.getresponse.return_value.status = status
        request_mock.getresponse.return_value.reason = reason
        request_mock.getresponse.return_value.read = lambda : response
        
    def test_OperationRaisesExceptionOnHTTPStatus500(self):
        self.force_http_status( 500, 'Forced Failure')
        op = self.service.get('http://{0}/'.format(HOSTNAME))
        self.assertRaises( HTTPError, op.execute)

    def test_OperationUsesGet(self):
        self.force_http_status( 200, 'Success')
        op = self.service.get('http://{0}/'.format(HOSTNAME))
        op.execute()
        self.mock_HTTPConnection().request.assert_called_with('GET', '/', '')
        
    def test_OperationSendsRequestData(self):
        self.force_http_status( 200, 'Success')
        test_data = 'abcdef'
        op = self.service.get('http://{0}/'.format(HOSTNAME), test_data)
        op.execute()
        self.mock_HTTPConnection().request.assert_called_with('GET', '/', test_data)       

    def test_OperationReturnsResponseData(self):
        response = 'sample response data'
        self.force_http_status( 200, 'Success', response)
        op = self.service.get('http://{0}/'.format(HOSTNAME), )
        op.execute()
        self.assertEqual( response, op.response)
         
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


class JSONRESTOperationTestCase(TestCase):
    def test_JSONRESTOperationWillEncodeDataToJSON(self):
        pass
