from unittest2 import TestCase
import edacloud_client.client
from mock import Mock

class ClientTestCase(TestCase):
    def setUp(self):
        self.original = edacloud_client.client.EDACloudService
        edacloud_client.client.EDACloudService = Mock(return_value=Mock(spec=self.original))
        self.client = edacloud_client.client.EDACloudClient()
        self.mock_service = self.client.service
        
    def tearDown(self):
        edacloud_client.client.EDACloudService = self.original
    
    def test_ClientWillCreateServiceObject(self):
        self.assertIsNotNone(self.client.service)

       
