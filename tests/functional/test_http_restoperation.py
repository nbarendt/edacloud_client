from unittest2 import TestCase
from edacloud_client.restoperation import RESTService
from http_test_utils import HttpTestServer, SimpleGETHTTPRequestHandler
import edacloud_client.restoperation

USER = 'nobody'

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
        service = RESTService(dict(username=USER))
        op = service.get('http://{0}:{1}/'.format(
            self.fake_server.hostname, self.fake_server.port))
        op.execute()
        self.assertEqual(TestHandler.resp, op.response)

    def test_OperationWillSendHeaders(self):
        expected_headers = {'x-test-1' : 'hi', 'x-test-2': 'bye'}
        class TestHandler(SimpleGETHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.end_headers()
                special_keys = [k for k in self.headers if k.startswith('x-')]
                resp = '/n'.join(['{0} {1}'.format(
                    x, self.headers[x]) for x in special_keys])
                self.wfile.write(resp)
                return
        self.fake_server.replace_request_handler_with(TestHandler)
        service = RESTService(dict(username=USER))
        op = service.get('http://{0}:{1}/'.format(self.fake_server.hostname,
            self.fake_server.port), '', expected_headers)
        op.execute()
        expected_response = '/n'.join(
            ['{0} {1}'.format(x, expected_headers[x]) 
                for x in expected_headers])
        self.assertEqual(expected_response, op.response)
