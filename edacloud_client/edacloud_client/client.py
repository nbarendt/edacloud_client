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
        raise Exception('SHOULD BE MOCKED!')
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

    def build_project(self, project_id):
        pass

    def get_build_results(self, build_id):
        pass

