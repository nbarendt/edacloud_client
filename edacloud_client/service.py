from urlparse import urljoin
from edacloud_client.restoperation import JSONRESTOperation

class Project(object):
    pass

class Build(object):
    def save_results_to_local_path(self, path):
        pass

class PingResult(object):
    def __init__(self, success, hostname, port):
        self.success = success
        self.hostname = hostname
        self.port = port

class EDACloudService(object):
    base_api_path = 'api'
    api_version = 'v2010-06-28'
    
    def __init__(self, hostname, port, username):
        self.hostname = hostname
        self.port = port
        self.username = username
        self._api_version_url = None
        self._user_url = None
        
    def find_required_api_version(self, desired_version, versions_list):
        for ver in versions_list:
            if desired_version in ver:
                return ver[desired_version]['href']
    
    @property
    def api_version_url(self):
        if not self._api_version_url:
            api_url = self.synthesize_entry_point_url()
            response = self.make_json_request('GET', api_url) 
            versions = response.data['links']['versions']
            self._api_version_url = self.find_required_api_version(
                self.api_version, versions) 
        return self._api_version_url

    @property
    def user_url(self):
        if not self._user_url:
            response = self.make_json_request('GET', self.api_version_url)
            self._user_url = response.data['links'][self.username]['href']
        return self._user_url

    def synthesize_entry_point_url(self):
        base_url = 'http://{0}:{1}'.format(self.hostname, self.port)
        return urljoin(base_url, self.base_api_path)

    def ping_server(self):
        url = self.synthesize_entry_point_url()    
        response = self.make_json_request('GET', url)
        ping_result = PingResult(response.result.status == 200,
            self.hostname, self.port)
        return ping_result 

    def make_json_request(self, method, url, data=''):
        headers = {'Accept' : 'application/json'}
        op = JSONRESTOperation(method, url, data, headers)
        op.execute()
        return  op
 
    def get_all_projects(self):
        pass

    def get_project_by_ID(self, project_id):
        pass

    def create_new_project(self, project_path):
        pass

    def build_project(self, project_id):
        pass

    def get_build_by_ID(self, build_id):
        pass
    
