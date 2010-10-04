from unittest2 import TestCase
import edacloud_client.client
import edacloud_client.service
from mock import Mock
from test_utils import MockFunctionHelper


class ClientTestCase(TestCase):
    default_server_params = dict(hostname='quidgybo', port=123, user='nobody')

    def setUp(self):
        self.original = edacloud_client.client.EDACloudService
        edacloud_client.client.EDACloudService = Mock(
            return_value=Mock(spec=self.original))
        for k in self.default_server_params.keys():
            setattr(edacloud_client.client.EDACloudClient,
                k, self.default_server_params[k])
        self.client = edacloud_client.client.EDACloudClient()
        self.mock_service = self.client.service
        
    def tearDown(self):
        edacloud_client.client.EDACloudService = self.original

    def service(self, attr):
        return MockFunctionHelper(getattr(self.mock_service, attr))

    def test_ClientWillCreateServiceObject(self):
        self.assertIsNotNone(self.client.service)

    def test_ClientWillCreateServiceObjectWithDefaultParams(self):
        expected = [
            ( (
                self.default_server_params['hostname'],
                self.default_server_params['port'],
                self.default_server_params['user']
                ), {} ),
            ]
        self.assertEqual( expected, 
            edacloud_client.client.EDACloudService.call_args_list)

    def test_ClientWillReturnEmptyProjectsList(self):
        self.service('get_all_projects').will_return([])
        self.assertListEqual([], self.client.get_project_list())

    def test_ClientWillRaiseExceptionOnGetProjectByIDWithBadID(self):
        self.service('get_project_by_ID').will_cause_side_effect(
            edacloud_client.client.BadProjectID('sample_bad_id'))
        self.assertRaises(edacloud_client.client.BadProjectID,
            self.client.get_project_by_ID, project_id=None)

    def test_ClientWillReturnProjectOnGetProjectByID(self):
        proj = edacloud_client.service.Project()
        self.service('get_project_by_ID').will_return(proj)
        self.assertEqual(proj, self.client.get_project_by_ID('testID'))

    def test_ClientWillAddNewProject(self):
        self.service('create_new_project').will_return(
            Mock(spec=edacloud_client.service.Project))
        project_path = 'testproject'
        self.client.add_project(project_path)
        self.service('create_new_project').was_called_with(
            [((project_path,), {})])

    def test_ClientWillBuildProject(self):
        build = edacloud_client.service.Build()
        self.service('build_project').will_return(build)
        self.assertEqual(build, self.client.build_project('testproject'))
       
    def test_ClientWillRaiseExceptionOnBuildProjectWithBadID(self):
        self.service('build_project').will_cause_side_effect(
            edacloud_client.client.BadProjectID('sample_bad_id'))
        self.assertRaises(edacloud_client.client.BadProjectID,
            self.client.build_project, project_id=None)

    def test_ClientWillGetBuildResults(self):
        build_id = 'aaa'
        target_dir = 'bbb'
        build = Mock(spec=edacloud_client.service.Build)
        build.save_results_to_local_path.return_value = target_dir
        self.service('get_build_by_ID').will_return(build)
        self.assertEqual(target_dir,
            self.client.get_build_results(build_id, target_dir))
        build.save_results_to_local_path.assert_called_with(target_dir)

