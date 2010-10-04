from edacloud_client.exceptions import *
from edacloud_client.service import EDACloudService


class EDACloudClient(object):
    hostname = ''
    port = 0
    user = ''

    def __init__(self):
        self.service = EDACloudService(self.hostname, self.port, self.user)

    def get_project_list(self):
        return self.service.get_all_projects()

    def get_project_by_ID(self, project_id):
        return self.service.get_project_by_ID(project_id)

    def add_project(self, project_path):
        return self.service.create_new_project(project_path)

    def build_project(self, project_id):
        return self.service.build_project(project_id)

    def get_build_results(self, build_id, target_dir):
        build = self.service.get_build_by_ID(build_id)
        return build.save_results_to_local_path(target_dir)
