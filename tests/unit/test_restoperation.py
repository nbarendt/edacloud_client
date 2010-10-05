from unittest2 import TestCase
from edacloud_client.restoperation import RESTOperation, JSONRESTOperation
from edacloud_client.exceptions import UnsupportedURLScheme, HTTPError
from mock import Mock, patch, mocksignature
import edacloud_client.restoperation

HOSTNAME = 'hostname.com'
PORT = 8080
USER = 'nobody'

class RESTOperationURLParsingTestCase(TestCase):
    def test_ServiceOperationWillRaiseExceptionOnUnsupportedScheme(self):
        self.assertRaises( UnsupportedURLScheme,
            RESTOperation, 'GET', 'ftp://')

    def test_OperationWillParsePath(self):
        expected_path = '/index'
        op = RESTOperation(None,
            'http://{0}{1}'.format(HOSTNAME, expected_path))
        self.assertEqual(expected_path, op.path)

    def test_OperationWillParseQueryString(self):
        expected_qs = 'hello=world&goodbye=world'
        op = RESTOperation(None,
            'http://{0}/?{1}'.format(HOSTNAME, expected_qs))
        self.assertEqual(expected_qs, op.query)

class RESTOperationHTTPBehaviorTestCase(TestCase):
    test_url = 'http://{0}/'.format(HOSTNAME)
    def setUp(self):
        self.original = edacloud_client.restoperation.HTTPConnection
        self.mock_HTTPConnection = Mock(spec=self.original)
        edacloud_client.restoperation.HTTPConnection = self.mock_HTTPConnection
        
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
        op = RESTOperation('GET', self.test_url)
        self.assertRaises( HTTPError, op.execute)

    def test_OperationUsesGet(self):
        self.force_http_status( 200, 'Success')
        op = RESTOperation('GET', self.test_url)
        op.execute()
        self.mock_HTTPConnection().\
            request.assert_called_with('GET', '/', '', {})
        
    def test_OperationSendsRequestData(self):
        self.force_http_status( 200, 'Success')
        test_data = 'abcdef'
        op = RESTOperation('GET', self.test_url, test_data)
        op.execute()
        self.mock_HTTPConnection().\
            request.assert_called_with('GET', '/', test_data, {})       

    def test_OperationReturnsResponseData(self):
        response = 'sample response data'
        self.force_http_status( 200, 'Success', response)
        op = RESTOperation('GET', self.test_url)
        op.execute()
        self.assertEqual( response, op.response)

    def test_OperationCallsPrepareForRequest(self):
        self.force_http_status( 200, 'Success')
        op = RESTOperation('GET', self.test_url)
        op.prepare_for_request = mocksignature(op.prepare_for_request)
        op.execute()
        self.assertTrue(op.prepare_for_request.mock.called)

class JSONRESTOperationEncodeDecodeTestCase(TestCase):
    test_url = 'http://{0}/'.format(HOSTNAME)
    test_data = { 'hello' : 'world', 'a' : [1,2,3] }
    test_data_str =  '{"a": [1, 2, 3], "hello": "world"}'

    def setUp(self):
        self.original = edacloud_client.restoperation.HTTPConnection
        self.mock_HTTPConnection = Mock(spec=self.original)
        edacloud_client.restoperation.HTTPConnection = self.mock_HTTPConnection
        
    def tearDown(self):
        edacloud_client.restoperation.HTTPConnection = self.original

    def force_http_status(self, status, reason, response=''):
        request_mock = self.mock_HTTPConnection()
        request_mock.getresponse.return_value = Mock()
        request_mock.getresponse.return_value.status = status
        request_mock.getresponse.return_value.reason = reason
        request_mock.getresponse.return_value.read = lambda : response

    def test_WillEncodeRequestDataAsJSON(self):
        self.force_http_status(200, 'Success')
        op = JSONRESTOperation('GET', self.test_url, self.test_data)
        op.execute()
        self.mock_HTTPConnection().\
            request.assert_called_with('GET', '/', self.test_data_str, {})
        
    def test_WillDecodeResponseDataAsJSON(self):
        self.force_http_status(200, 'Success', self.test_data_str)
        op = JSONRESTOperation('GET', self.test_url)
        op.execute()
        self.assertEqual(self.test_data, op.response)



