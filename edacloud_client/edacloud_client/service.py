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
        
    def filter_api_versions(self, desired_version, versions_list):
        for ver in versions_list:
            if desired_version in ver:
                return ver[desired_version]['href']
        raise Exception('Unable to locate required API version')
    
    def get_api_version_url(self):
        api_url = '/'.join(['http://{0}:{1}'.format(self.hostname, self.portnumber), self.base_api_path])
        results = self.make_request('GET', api_url)
        return self.filter_api_versions(self.api_version, results['links']['versions'])

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
    
