
class BadProjectID(Exception):
    def __init__(self, project_id):
        self.project_id = project_id

    def __str__(self):
        return 'Bad Project ID: {0}'.format(self.project_id)

class BadBuildID(Exception):
    def __init__(self, build_id):
        self.build_id = build_id

    def __str__(self):
        return 'Bad Build ID: {0}'.format(self.build_id)

class BuildException(Exception):
    def __init__(self, project_id, build_id, details):
        self.project_id = project_id
        self.build_id = build_id
        self.details = details

    def __str__(self):
        return 'Build Exception on Build {0} for Project {1}: {2}'.format(self.project_id,
                                                                          self.build_id,
                                                                          self.details)
