from unittest2 import TestCase
from subprocess import Popen, PIPE, STDOUT
from time import sleep
import os
from StringIO import StringIO
from edacloud_client.cli import EDACloudCLIClient
import BaseHTTPServer
from threading import Thread
import json

python_exe = 'python'

MODULE_NAME = 'edacloud_client'
CLI_NAME = 'cli.py'

ECHO_CMD = 'echo'
QUIT_CMD = 'quit'

ECHO_LINE = 'Hello!'
TEST_ECHO_CMDLINE = '{0} {1}'.format(ECHO_CMD, ECHO_LINE)

class PopenCLITestCase(TestCase):
    def test_WillEcho(self):
        cmdline = [python_exe, os.path.join(MODULE_NAME, CLI_NAME)]
        proc = Popen(cmdline, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
        stdoutdata, stderrdata = proc.communicate('\n'.join([TEST_ECHO_CMDLINE , QUIT_CMD]))
        self.assertIn(ECHO_LINE, stdoutdata, 'cmd.py failed to echo')

class HttpTestServer(object):
    def __init__(self):
        self.httpd_server = BaseHTTPServer.HTTPServer(('localhost', 0), BaseHTTPServer.BaseHTTPRequestHandler)
        self.server_thread = Thread(target=self.httpd_server.serve_forever)
        self.server_thread.daemon = True

    def get_server_address(self):
        return self.httpd_server.server_address

    def start(self):
        self.server_thread.start()

    def stop(self):
        if self.server_thread.isAlive():
            self.httpd_server.shutdown()
            self.server_thread.join()
            self.server_thread = None

    def replace_request_handler_with(self, request_handler):
        self.httpd_server.RequestHandlerClass = request_handler

class CLIApplication(object):
    def __init__(self, server):
        self.stdout_buffer = StringIO()
        self.cmd = EDACloudCLIClient(stdout=self.stdout_buffer)
        self.cmd.server_hostname = server.get_server_address()[0]
        self.cmd.server_portnumber = server.get_server_address()[1]

    @property
    def display(self):
        return self.stdout_buffer.getvalue()

    def issue_command(self, cmdline):
        self.cmd.onecmd(cmdline)
        return self

    def shows(self, expected):
        assert expected in self.display, 'Failed to find "%s" in "%s"' % (expected, self.display)
        return self

    def get_datetime(self):
        self.issue_command('datetime')
        return self

    def get_project_list(self):
        self.issue_command('projects')
        return self
    
    def add_project(self, project_path):
        self.issue_command('add {0}'.format(project_path))
        return self

class CLITestCase(TestCase):
    def setUp(self):
        self.fake_server = HttpTestServer()
        self.application = CLIApplication(self.fake_server)
        self.fake_server.start()

    def tearDown(self):
        self.application = None
        self.fake_server.stop()

    def test_WillGetListOfProjectsFromServer(self):
        class TestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps([]))
                return
        self.fake_server.replace_request_handler_with(TestHandler)
        self.application.get_project_list().shows('Projects:\n\n')
        
    def test_WillAddProjectToServer(self):
        PROJECT_FILESYSTEM_PATH = 'c:\quidgyboo'
        project_list = []
        class TestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps(project_list))
                return

            def do_POST(self):
                content_length = int(self.headers.get('Content-Length', '0'))
                assert content_length != 0
                req = json.loads(self.rfile.read(content_length))
                new_url = '/'.join([self.path, '1'])
                project_list.append(dict(path=req['path'],
                                          href=new_url))
                self.send_response(201)
                self.end_headers()
                self.wfile.write(json.dumps(project_list[0]))
                return

        self.fake_server.replace_request_handler_with(TestHandler)
        self.application.add_project(PROJECT_FILESYSTEM_PATH).shows('\n')
        self.application.get_project_list().shows('Projects:\n{0}\n'.format(PROJECT_FILESYSTEM_PATH))


        
                         
