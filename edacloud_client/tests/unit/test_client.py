from unittest2 import TestCase
import edacloud_client.client
from mock import Mock

class ClientTestCase(TestCase):
    def setUp(self):
        self.original = edacloud_client.client.EDACloudService
        edacloud_client.client.EDACloudService = Mock()

    def tearDown(self):
        edacloud_client.client.EDACloudService = self.original
    
    def test_ClientCreatesServiceObject(self):
        self.assertIsNotNone(edacloud_client.client.EDACloudClient().service)
