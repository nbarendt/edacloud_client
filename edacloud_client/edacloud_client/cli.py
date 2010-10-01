#!/usr/bin/env python 
from cmd import Cmd
import sys
from edacloud_client.client import EDACloudClient
from edacloud_client.exceptions import *


class EDACloudCLI(Cmd):
    prompt = 'edacloud> '

    def __init__(self, completekey='tab', stdin=None, stdout=None, asyncout=None, client_class=None):
        Cmd.__init__(self, completekey, stdin, stdout)
        self.asyncout = asyncout if asyncout else stdout if stdout else sys.stdout
	self.stdout = stdout if stdout else  sys.stdout
	self.stderr = sys.stderr
        self._client =  None

    @property
    def client(self):
        self._client = self._client or self.make_client()
	return self._client

    def make_client(self):
        client = EDACloudClient()
        client.build_event_status_handler = self.async_build_event_status_handler
        return client
   
    def async_build_event_status_handler(self, project, build, status):
        self.asyncout.write('Build Status: {status[message]} for build started at {build[started]}\n'.format(
                project=project, build=build, status=status))

    def do_quit(self, args):
        self.stdout.write('bye!\n')
        return True

    def do_EOF(self, args):
        return self.do_quit(args)

    def do_projects(self, args):
        self.stdout.write('Projects:\n')
        for proj in self.client.get_project_list():
            self.stdout.write(':'.join([proj.id, proj.path]))
            self.stdout.write('\n')
        self.stdout.write('\n')

    def do_add(self, args):
        self.client.add_project(args)
        self.stdout.write('\n')

    def do_build(self, args):
        try:
            self.client.build_project(args)
            self.stdout.write('\n')
        except BadProjectID, e:
            self.stdout.write('Error Building Project: Unknown Project ID {0}\n'.format(e.id))
        except BuildException, e:
            self.stdout.write('Error Building Project: %s %s\n' % (e.details, e.project_id))
                              
    def do_get(self, args):
        args_list = args.split()
        if len(args_list) != 2:
            self.stdout.write('Error parsing "get {0}"\n'.format(args))
            return
        build_id = args_list[0]
        target_dir = args_list[1]
        try:
            results = self.client.get_build_results(build_id, target_dir)
            self.stdout.write('Build {0} results available in {1}\n'.format(build_id, results))
        except BadBuildID, e:
            self.stdout.write('Error Retrieving Results:  Unknown Build ID {0}\n'.format(e.id))

class TestCLI(EDACloudCLI):
    def postcmd(self, stop, line):
        self.stdout.write("OK\n")
        self.stdout.flush()
	self.stderr.flush()
	return stop

def test_main():
    cli = TestCLI()
    try:
        cli.cmdloop()
    except  IOError:
        pass

def main():
    cli = EDACloudCLI()
    cli.cmdloop()    

if __name__ == '__main__':
	main()    
