from unittest2 import TestCase
from mock import Mock, patch
from edacloud_client.cli import EDACloudCLI
from StringIO import StringIO

class CLIApplication(object):
    def __init__(self):
        self.stdout_buffer = StringIO()
        self.cmd = EDACloudCLI(stdout=self.stdout_buffer)

    @property
    def display(self):
        return self.stdout_buffer.getvalue()

    def issue_command(self, cmdline):
        self.cmd.onecmd(cmdline)
        return self

    def shows(self, expected):
        assert expected in self.display, 'Failed to find "%s" in "%s"' % (expected, self.display)
        return self

    def get_project_list(self):
        self.issue_command('projects')
        return self
    
    def add_project(self, project_path):
        self.issue_command('add {0}'.format(project_path))
        return self

    def build_project(self, project_id):
        self.issue_command('build {0}'.format(project_id))
        return self

class CLITestCase(TestCase):
    def setUp(self):
        self.application = CLIApplication()

    def tearDown(self):
        self.application = None

    @patch('edacloud_client.cli.EDACloudClient', spec=['get_project_list'])
    def test_ClientWillReturnEmptyProjectList(self, MockClient):
        instance = MockClient()
        instance.get_project_list.return_value = []
        self.application.get_project_list().shows('Projects:\n\n')

    @patch('edacloud_client.cli.EDACloudClient', spec=['get_project_list'])
    def test_ClientWillReturnNonEmptyProjectList(self, MockClient):
        instance = MockClient()
        instance.get_project_list.return_value = [ {'path': 'a', 'id': '12'},
                                                   {'path': 'b', 'id': '34'},
                                                   {'path': 'c', 'id': '56'}
                                                   ]
        self.application.get_project_list().shows('Projects:\n12:a\n34:b\n56:c\n')

    @patch('edacloud_client.cli.EDACloudClient', spec=['add_project'])
    def test_ClientWillAddProject(self, MockClient):
        PROJECT_FILESYSTEM_PATH = 'c:\quidgyboo'
        instance = MockClient()
        self.application.add_project(PROJECT_FILESYSTEM_PATH).shows('\n')
        self.assertListEqual(instance.add_project.call_args_list, [((PROJECT_FILESYSTEM_PATH,), {} )])

    @patch('edacloud_client.cli.EDACloudClient', spec=['build_project'])
    def test_ClientWillBuildProject(self, MockClient):
        PROJECT_ID = 'abcdefg'
        instance = MockClient()
        self.application.build_project(PROJECT_ID).shows('\n')
        self.assertListEqual(instance.build_project.call_args_list, [((PROJECT_ID,), {} )])

    @patch('edacloud_client.cli.EDACloudClient', spec=['build_project'])
    def test_ClientWillErrorOnInvalidProjectID(self, MockClient):
        PROJECT_ID = 'abcdefg'
        instance = MockClient()
        exc = Exception('Unknown Project ID')
        exc.project_id = PROJECT_ID
        instance.build_project.side_effect = exc
        self.application.build_project(PROJECT_ID).shows('Error Building Project: Unknown Project ID %s\n' % PROJECT_ID)



