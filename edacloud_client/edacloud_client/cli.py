#!/usr/bin/env python 
from cmd import Cmd
from urllib2 import urlopen
import json
from urlparse import urlparse, urlunparse
from httplib import HTTPConnection
import sys

def make_request(method, url, data=''):
    (scheme, netloc, path, params, query, fragment) = urlparse(url)
    if scheme != 'http':
        raise Exception('Unsupported URL scheme: %s' % scheme)
    try:
        host, port = netloc.split(':', 1)
    except ValueError:
        host = netloc
        port = 80
    
    conn = HTTPConnection(host, int(port))
    conn.request(method, path, data)
    result = conn.getresponse()
    if result.status not in [200, 201, 204]:
        raise Exception('%s on %s returned status of %s with '
                        'response body of %s' % (
                method, url, result.status, result.read()))
    return result

class EDACloudClient(object):
    def __init__(self, hostname, portnumber, username):
        self.server_hostname = hostname
        self.server_portnumber = portnumber
        self.username = username
        self.build_event_status_handler = None

    def get_user(self, path):
        url = 'http://{0}:{1}/{2}/{3}'.format(self.server_hostname, self.server_portnumber, self.username, path)
        return make_request('GET', url)

    def post_user_json(self, path, data):
        url = 'http://{0}:{1}/{2}/{3}'.format(self.server_hostname, self.server_portnumber, self.username, path)
        return make_request('POST', url, json.dumps(data))

    def get_project_list(self):
        try:
            return json.loads(self.get_user('projects').read())
        except ValueError:
            return []

    def add_project(self, project_path):
        self.post_user_json('projects', dict(path=project_path.strip())).read()
        return

class BuildException(Exception):
    def __init__(self, details, project_id):
        self.details = details
        self.project_id = project_id

class EDACloudCLI(Cmd):
    prompt = 'edacloud> '
    server_hostname = 'localhost'
    server_portnumber = 8080
    username = 'nobody'

    def __init__(self, completekey='tab', stdin=None, stdout=None, asyncout=None, client_class=None):
        Cmd.__init__(self, completekey, stdin, stdout)
        self.asyncout = asyncout if asyncout else stdout if stdout else sys.stdout
        self.client =  self.make_client(client_class if client_class else EDACloudClient)

    def make_client(self, client_class):
        client = client_class(self.server_hostname, self.server_portnumber, self.username)
        client.build_event_status_handler = self.async_build_event_status_handler
        return client
   
    def async_build_event_status_handler(self, project, build, status):
        self.asyncout.write('Build Status: {status[message]} for build started at {build[started]}'.format(
                project=project, build=build, status=status))

    def do_quit(self, args):
        self.stdout.write('bye!\n')
        return True

    def do_EOF(self, args):
        return self.do_quit(args)

    def do_projects(self, args):
        self.stdout.write('Projects:\n')
        for proj in self.client.get_project_list():
            self.stdout.write(':'.join([proj['id'], proj['path']]))
            self.stdout.write('\n')
        self.stdout.write('\n')

    def do_add(self, args):
        self.client.add_project(args)
        self.stdout.write('\n')

    def do_build(self, args):
        try:
            self.client.build_project(args)
            self.stdout.write('\n')
        except BuildException, e:
                self.stdout.write('Error Building Project: %s %s\n' % (e.details, e.project_id))

    def do_get(self, args):
        args_list = args.split()
        build_id = args_list[0]
        target_dir = args_list[1]
        results = self.client.get_build_results(build_id, target_dir)
        self.stdout.write('Build {0} results available in {1}'.format(build_id, results))
        
if __name__ == '__main__':
    cli = EDACloudCLIClient()
    cli.cmdloop()
