from unittest2 import TestCase
from mock import Mock, patch
import edacloud_client.cli
from StringIO import StringIO
from datetime import datetime

class CLIApplication(object):
    def __init__(self):
        self.stdout_buffer = StringIO()
        self.async_buffer = StringIO()
        self.cmd = edacloud_client.cli.EDACloudCLI(stdout=self.stdout_buffer,
                                                   asyncout=self.async_buffer,
                                                   client_class=Mock())
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
        return ClientFunctionMock(getattr(self.mock_client, attr))

class ClientFunctionMock(object):
    def __init__(self, func):
        self.func = func

    def returns(self, value):
        setattr(self.func, 'return_value', value)

    def has_side_effect(self, value):
        setattr(self.func, 'side_effect', value)

    def was_called_with(self, expected):
        actual = getattr(self.func, 'call_args_list')
        assert expected == actual 
    
class CLITestCase(TestCase):
    def setUp(self):
        self.application = CLIApplication()

    def tearDown(self):
        self.application = None

    def test_ClientWillReturnEmptyProjectList(self):
        self.application.client('get_project_list').returns([])
        self.application.get_project_list().shows('Projects:\n\n')

    def test_ClientWillReturnNonEmptyProjectList(self):
        self.application.client('get_project_list').returns( [ {'path': 'a', 'id': '12'},
                                                               {'path': 'b', 'id': '34'},
                                                               {'path': 'c', 'id': '56'}
                                                               ])
        self.application.get_project_list().shows('Projects:\n12:a\n34:b\n56:c\n')

    def test_ClientWillAddProject(self):
        PROJECT_FILESYSTEM_PATH = 'c:\quidgyboo'
        self.application.add_project(PROJECT_FILESYSTEM_PATH).shows('\n')
        self.application.client('add_project').was_called_with([((PROJECT_FILESYSTEM_PATH,), {} )])

    def test_ClientWillBuildProject(self):
        PROJECT_ID = 'abcdefg'
        self.application.build_project(PROJECT_ID).shows('\n')
        self.application.client('build_project').was_called_with([((PROJECT_ID,), {} )])

    def test_ClientWillErrorOnInvalidProjectID(self):
        PROJECT_ID = 'abcdefg'
        self.application.client('build_project').has_side_effect(edacloud_client.cli.BuildException(
            'Unknown Project ID', PROJECT_ID))
        self.application.build_project(PROJECT_ID).shows(
            'Error Building Project: Unknown Project ID %s\n' % PROJECT_ID)

    def test_ClientWillRegisterBuildStatusHandler(self):
        self.assertIsNotNone(self.application.mock_client.build_event_status_handler)

    def test_ClientWillReportAsyncBuildStatusEvent(self):
        started_date_time = datetime.now().isoformat()
        project = dict()
        build = dict(started=started_date_time)
        status = dict(message='Complete')
        self.application.force_async_build_event_status(project, build, status)
        self.application.async_shows('Build Status: Complete for build started at {0}'.format(started_date_time))

    def test_ClientWillDownloadBuildResults(self):
        BUILD_ID = 'abcdefg'
        DOWNLOAD_DIR = 'c:\quidgybo\download_build'
        self.application.client('get_build_results').returns(DOWNLOAD_DIR)
        self.application.get_build_results(BUILD_ID, DOWNLOAD_DIR).shows(
            'Build {0} results available in {1}'.format(BUILD_ID, DOWNLOAD_DIR))
        self.application.client('get_build_results').was_called_with([ ((BUILD_ID, DOWNLOAD_DIR), {} )])
