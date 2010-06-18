from unittest2 import TestCase
from subprocess import Popen, PIPE, STDOUT
from time import sleep
import os
from StringIO import StringIO
from edacloud_client.cli import EDACloudClient

python_exe = 'python'

MODULE_NAME = 'edacloud_client'
CLI_NAME = 'cli.py'

ECHO_CMD = 'echo'
QUIT_CMD = 'quit'

ECHO_LINE = 'Hello!'
TEST_ECHO_LINE = '{0} {1}'.format(ECHO_CMD, ECHO_LINE)

class PopenCLITestCase(TestCase):
    def test_WillEcho(self):

        cmdline = [python_exe, os.path.join(MODULE_NAME, CLI_NAME)]
        proc = Popen(cmdline, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
        stdoutdata, stderrdata = proc.communicate('\n'.join([TEST_ECHO_LINE , QUIT_CMD]))
        self.assertIn(ECHO_LINE, stdoutdata, 'cmd.py failed to echo')

class CLITestCase(TestCase):
    def setUp(self):
        self.stdout_buffer = StringIO()
        self.cmd = EDACloudClient(stdout=self.stdout_buffer)

    def tearDown(self):
        self.cmd = None
        self.stdout_buffer.close()
        self.stdout_buffer = None

    def test_WillEcho(self):
        self.cmd.onecmd(TEST_ECHO_LINE)
        self.assertIn(ECHO_LINE, self.stdout_buffer.getvalue())
                         
