from edacloud_client.exceptions import *
from edacloud_client.service import EDACloudService


class EDACloudClient(object):
    def __init__(self, hostname, port, user):
        self.service = EDACloudService(hostname, port, user)

    def ping_server(self):
        return self.service.ping_server()

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
