class Project(object):
    pass

class Build(object):
    def save_results_to_local_path(self, path):
        pass

class EDACloudService(object):
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
    
