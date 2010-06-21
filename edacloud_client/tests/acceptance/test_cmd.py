from unittest2 import TestCase
from subprocess import Popen, PIPE, STDOUT
from time import sleep
import os
from StringIO import StringIO
from edacloud_client.cli import EDACloudClient
import BaseHTTPServer
from threading import Thread

python_exe = 'python'

MODULE_NAME = 'edacloud_client'
CLI_NAME = 'cli.py'

ECHO_CMD = 'echo'
QUIT_CMD = 'quit'

ECHO_LINE = 'Hello!'
TEST_ECHO_CMDLINE = '{0} {1}'.format(ECHO_CMD, ECHO_LINE)
EXPECTED_DATETIME_ISO_STRING = '2010-06-21T10:49:49.230427'

class PopenCLITestCase(TestCase):
    def test_WillEcho(self):
        cmdline = [python_exe, os.path.join(MODULE_NAME, CLI_NAME)]
        proc = Popen(cmdline, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
        stdoutdata, stderrdata = proc.communicate('\n'.join([TEST_ECHO_CMDLINE , QUIT_CMD]))
        self.assertIn(ECHO_LINE, stdoutdata, 'cmd.py failed to echo')


class CLITestCase(TestCase):
    def setUp(self):
        self.stdout_buffer = StringIO()
        self.cmd = EDACloudClient(stdout=self.stdout_buffer)
        self.httpd_server = None

    def tearDown(self):
        self.cmd = None
        self.stdout_buffer.close()
        self.stdout_buffer = None
        self.stop_http_test_server()

    def start_http_test_server(self, req_handler):
        self.server_hostname = 'localhost'
        self.server_portnumber = 0
        self.httpd_server = BaseHTTPServer.HTTPServer( (self.server_hostname, self.server_portnumber),
                                                        req_handler)
        self.cmd.server_hostname = self.httpd_server.server_address[0]
        self.cmd.server_portnumber = self.httpd_server.server_address[1]
        self.server_thread = Thread(target=self.httpd_server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()        

    def stop_http_test_server(self):
        if self.httpd_server:
            self.httpd_server.shutdown()
            self.server_thread.join()
            self.server_thread = None
            self.httpd_server = None

    def test_WillEcho(self):
        self.cmd.onecmd(TEST_ECHO_CMDLINE)
        self.assertIn(ECHO_LINE, self.stdout_buffer.getvalue())

    def test_WillGetTimeFromServer(self):
        GET_TIME_CMDLINE = 'datetime'
        class GetDateTimeTestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.end_headers()
                self.wfile.write(EXPECTED_DATETIME_ISO_STRING)
                return
        self.start_http_test_server(GetDateTimeTestHandler)
        self.cmd.onecmd(GET_TIME_CMDLINE)
        self.assertEquals(EXPECTED_DATETIME_ISO_STRING, self.stdout_buffer.getvalue())


                         
