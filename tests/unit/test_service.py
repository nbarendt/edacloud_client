from unittest2 import TestCase
from edacloud_client.service import EDACloudService
from mock import Mock, mocksignature

API_BASE = 'api'
VERSION = 'v2010-06-28'
USER = 'nobody'

HOSTNAME = 'hostname.com'
PORT = 8080

class ServiceInitTestCase(TestCase):
    def test_ServiceWillReturnSpecifiedHostNmae(self):
        service = EDACloudService(HOSTNAME, PORT, USER)
        self.assertEqual(HOSTNAME, service.hostname)
        self.assertEqual(PORT, service.port)

