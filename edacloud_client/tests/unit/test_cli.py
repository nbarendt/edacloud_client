from unittest2 import TestCase
from mock import Mock, patch
import edacloud_client.cli
import edacloud_client.client
from StringIO import StringIO
from datetime import datetime
from test_utils import MockFunctionHelper

class CLIApplication(object):
    def __init__(self):
        self.stdout_buffer = StringIO()
        self.async_buffer = StringIO()
        self.cmd = edacloud_client.cli.EDACloudCLI(stdout=self.stdout_buffer, asyncout=self.async_buffer)
        self.mock_client = self.cmd.client

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

    def get_build_results(self, build_id, results_dir):
        self.issue_command('get {0} {1}'.format(build_id, results_dir))
        return self
    
    def force_async_build_event_status(self, project, build, status):
        self.mock_client.build_event_status_handler(project, build, status)

    def client(self, attr):
        return MockFunctionHelper(getattr(self.mock_client, attr))
    
class CLITestCase(TestCase):
    def setUp(self):
        self.original = edacloud_client.cli.EDACloudClient
        edacloud_client.cli.EDACloudClient = Mock(return_value=Mock(spec=self.original))
        self.application = CLIApplication()

    def tearDown(self):
        self.application = None
        edacloud_client.cli.EDACloudClient = self.original

    def test_CLIWillReturnEmptyProjectList(self):
        self.application.client('get_project_list').will_return([])
        self.application.get_project_list().shows('Projects:\n\n')

    def test_CLIWillReturnNonEmptyProjectList(self):
        projects_list = [Mock(), Mock()]
        projects_list[0].path = 'a'
        projects_list[0].id = '12'
        projects_list[1].path = 'b'
        projects_list[1].id = '34'
        self.application.client('get_project_list').will_return( projects_list)
        self.application.get_project_list().shows('Projects:\n12:a\n34:b\n')

    def test_CLIWillAddProject(self):
        self.application.add_project('c:\quidgyboo').shows('\n')

    def test_CLIWillBuildProject(self):
        self.application.build_project('abcdefg').shows('\n')

    def test_CLIWillErrorOnInvalidProjectID(self):
        PROJECT_ID = 'abcdefg'
        self.application.client('build_project').will_cause_side_effect(edacloud_client.cli.BadProjectID(
            PROJECT_ID))
        self.application.build_project(PROJECT_ID).shows(
            'Error Building Project: Unknown Project ID %s\n' % PROJECT_ID)

    def test_CLIWillRegisterBuildStatusHandler(self):
        self.assertIsNotNone(self.application.mock_client.build_event_status_handler)

    def test_CLIWillReportAsyncBuildStatusEvent(self):
        started_date_time = datetime.now().isoformat()
        project = dict()
        build = dict(started=started_date_time)
        status = dict(message='Complete')
        self.application.force_async_build_event_status(project, build, status)
        self.application.async_shows('Build Status: Complete for build started at {0}\n'.format(started_date_time))

    def test_CLIWillDownloadBuildResults(self):
        BUILD_ID = 'abcdefg'
        DOWNLOAD_DIR = 'c:\quidgybo\download_build'
        self.application.client('get_build_results').will_return(DOWNLOAD_DIR)
        self.application.get_build_results(BUILD_ID, DOWNLOAD_DIR).shows(
            'Build {0} results available in {1}\n'.format(BUILD_ID, DOWNLOAD_DIR))

    def test_CLIWillErrorOnInvalidBuildIDOnDownloadBuildResults(self):
        exc = edacloud_client.cli.BadBuildID('bad_id')
        self.application.client('get_build_results').will_cause_side_effect(exc)
        self.application.get_build_results('build_id', 'target_dir').shows(
            'Error Retrieving Results:  Unknown Build ID bad_id\n')

    def test_CLIErrorOnBuildIDWithEmbeddedSpaces(self):
        BUILD_ID = 'abcd efg'
        DOWNLOAD_DIR = 'c:\quidgybo\download_build'
        self.application.get_build_results(BUILD_ID, DOWNLOAD_DIR).shows(
            'Error parsing "get {0} {1}"\n'.format(BUILD_ID, DOWNLOAD_DIR))

    def test_CLIErrorOnDownloadDirWithEmbeddedSpaces(self):
        BUILD_ID = 'abcdefg'
        DOWNLOAD_DIR = 'c:\qui dgybo\download_build'
        self.application.get_build_results(BUILD_ID, DOWNLOAD_DIR).shows(
            'Error parsing "get {0} {1}"\n'.format(BUILD_ID, DOWNLOAD_DIR))

