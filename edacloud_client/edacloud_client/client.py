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
        pass

    def get_project_list(self):
        pass
    
    def add_project(self, project_path):
        pass

    def build_project(self, project_id):
        pass

    def get_build_results(self, build_id):
        pass

