from urlparse import urljoin

class Project(object):
    pass

class Build(object):
    def save_results_to_local_path(self, path):
        pass

class EDACloudService(object):
    base_api_path = 'api'
    api_version = 'v2010-06-28'
    
    def __init__(self, hostname, portnumber, username):
        self.hostname = hostname
        self.portnumber = portnumber
        self.username = username
        self.api_version_url = self.get_api_version_url()
        self.user_url = self.get_user_url()
        
    def find_required_api_version(self, desired_version, versions_list):
        for ver in versions_list:
            if desired_version in ver:
                return ver[desired_version]['href']
    
    def get_api_version_url(self):
        base_url = 'http://{0}:{1}'.format(self.hostname, self.portnumber)
        api_url = urljoin(base_url, self.base_api_path)
        results = self.make_request('GET', api_url)
        versions = results['links']['versions']
        return self.find_required_api_version(self.api_version, versions) 

    def get_user_url(self):
        results = self.make_request('GET', self.api_version_url)
        return results['links'][self.username]['href']
        
    def make_request(self, method, url, data=''):
        pass
    
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
    
