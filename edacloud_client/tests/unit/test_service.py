from unittest2 import TestCase
from edacloud_client.service import EDACloudService
from mock import Mock, mocksignature

API_BASE = 'api'
VERSION = 'v2010-06-28'
USER = 'nobody'

HOSTNAME = 'hostname.com'
PORT = 8080

class ServiceInitTestCase(TestCase):
    def test_ServiceWillGetUserLink(self):
        HTTP_BASE = 'http://{0}:{1}'.format(HOSTNAME, PORT)
        versions_list = [ { VERSION : {'href' : '/'.join([HTTP_BASE, API_BASE, VERSION])}, }, ]
        EDACloudService.make_request = mocksignature(EDACloudService.make_request)
        responses = [ 
            { 'links' : { USER : {'href' : '/'.join([HTTP_BASE, API_BASE, VERSION, USER])} },} ,
            { 'links' : { 'versions' : versions_list }, },
            ]
        def return_response(self, method, url, data):
            return responses.pop()
        EDACloudService.make_request.mock.side_effect = return_response
        service = EDACloudService(HOSTNAME, PORT, USER)
        service.make_request.mock.assert_called_with(service, 'GET', '/'.join([HTTP_BASE, API_BASE, VERSION]), '')
        self.assertEqual('/'.join([HTTP_BASE, API_BASE, VERSION, USER]), service.user_url)
