from unittest2 import TestCase
from edacloud_client.restoperation import RESTService
from http_test_utils import HttpTestServer, SimpleGETHTTPRequestHandler
import edacloud_client.restoperation

         
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


