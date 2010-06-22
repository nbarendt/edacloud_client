#!/usr/bin/env python 
from cmd import Cmd
from urllib2 import urlopen
import json
from urlparse import urlparse, urlunparse
from httplib import HTTPConnection


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

class EDACloudCLI(Cmd):
    prompt = 'edacloud> '
    server_hostname = 'localhost'
    server_portnumber = 8080
    username = 'default'

    def __init__(self, completekey='tab', stdin=None, stdout=None):
        Cmd.__init__(self, completekey, stdin, stdout)
        self._client = None

    @property
    def client(self):
        if not self._client:
            self._client = EDACloudClient(self.server_hostname, self.server_portnumber, self.username)
        return self._client

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
        except Exception, e:
            if e.message == 'Unknown Project ID':
                self.stdout.write('Error Building Project: %s %s\n' % (e.message, e.project_id))


if __name__ == '__main__':
    cli = EDACloudCLIClient()
    cli.cmdloop()
