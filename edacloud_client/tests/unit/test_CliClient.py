from unittest2 import TestCase
from mock import Mock, patch
import edacloud_client.cli
from StringIO import StringIO
from datetime import datetime

class CLIApplication(object):
    def __init__(self):
        self.stdout_buffer = StringIO()
        self.async_buffer = StringIO()
        self.cmd = edacloud_client.cli.EDACloudCLI(stdout=self.stdout_buffer, asyncout=self.async_buffer)

    @property
    def display(self):
        return self.stdout_buffer.getvalue()

    @property
    def async_display(self):
        return self.async_buffer.getvalue()

    def issue_command(self, cmdline):
        self.cmd.onecmd(cmdline)
        return self

    def shows(self, expected):
        assert expected in self.display, 'Failed to find "%s" in "%s"' % (expected, self.display)
        return self

    def async_shows(self, expected):
        assert expected in self.async_display, 'Failed to find "%s" in "%s"' % (expected, self.async_display)
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

    def force_async_build_event_status(self, project, build, status):
        self.cmd

class CLITestCase(TestCase):
    @patch('edacloud_client.cli.EDACloudClient', spec=['get_project_list'])
    def test_ClientWillReturnEmptyProjectList(self, MockClient):
        application = CLIApplication()
        MockClient().get_project_list.return_value = []
        application.get_project_list().shows('Projects:\n\n')

    @patch('edacloud_client.cli.EDACloudClient', spec=['get_project_list'])
    def test_ClientWillReturnEmptyProjectList(self, MockClient):
        application = CLIApplication()
        MockClient().get_project_list.return_value = []
        application.get_project_list().shows('Projects:\n\n')

    @patch('edacloud_client.cli.EDACloudClient', spec=['get_project_list'])
    def test_ClientWillReturnNonEmptyProjectList(self, MockClient):
        application = CLIApplication()
        MockClient().get_project_list.return_value = [ {'path': 'a', 'id': '12'},
                                                       {'path': 'b', 'id': '34'},
                                                       {'path': 'c', 'id': '56'}
                                                       ]
        application.get_project_list().shows('Projects:\n12:a\n34:b\n56:c\n')

    @patch('edacloud_client.cli.EDACloudClient', spec=['add_project'])
    def test_ClientWillAddProject(self, MockClient):
        application = CLIApplication()
        PROJECT_FILESYSTEM_PATH = 'c:\quidgyboo'
        application.add_project(PROJECT_FILESYSTEM_PATH).shows('\n')
        self.assertListEqual(MockClient().add_project.call_args_list, [((PROJECT_FILESYSTEM_PATH,), {} )])

    @patch('edacloud_client.cli.EDACloudClient', spec=['build_project'])
    def test_ClientWillBuildProject(self, MockClient):
        PROJECT_ID = 'abcdefg'
        application = CLIApplication()
        application.build_project(PROJECT_ID).shows('\n')
        self.assertListEqual(MockClient().build_project.call_args_list, [((PROJECT_ID,), {} )])

    @patch('edacloud_client.cli.EDACloudClient', spec=['build_project'])
    def test_ClientWillErrorOnInvalidProjectID(self, MockClient):
        PROJECT_ID = 'abcdefg'
        exc = Exception('Unknown Project ID')
        exc.project_id = PROJECT_ID
        application = CLIApplication()
        MockClient().build_project.side_effect = exc
        application.build_project(PROJECT_ID).shows(
            'Error Building Project: Unknown Project ID %s\n' % PROJECT_ID)

    @patch('edacloud_client.cli.EDACloudClient')
    def test_ClientWillRegisterBuildStatusHandler(self, MockClient):
        self.assertIsNotNone(MockClient().build_event_status_handler)

    @patch('edacloud_client.cli.EDACloudClient')
    def test_ClientWillReportAsyncBuildStatusEvent(self, MockClient):
        #started_date_time = datetime.now().isoformat()
        #self.applicaiton.async_shows('Build Status: Complete for build started at 
        pass
