class UnsupportedURLScheme(Exception):
    def __init__(self, unsupported_scheme):
        self.scheme = unsupported_scheme

    def __str__(self):
        return 'Unsupported Scheme: {0}'.format(self.scheme)

class HTTPError(Exception):
    def __init__(self, status, reason):
        self.status = status
        self.reason = reason

    def __str__(self):
        return 'HTTP Server Returned {0} : {1}'.format(self.status, self.reason)

class BadProjectID(Exception):
    id_type = 'Project'
    def __init__(self, id):
        self.id = id

    def __str__(self):
        return 'Bad {0} ID: {1}'.format(self.id_type, self.id)

class BadBuildID(BadProjectID):
    id_type = 'Build'

class BuildException(Exception):
    def __init__(self, project_id, build_id, details):
        self.project_id = project_id
        self.build_id = build_id
        self.details = details

    def __str__(self):
        return 'Build Exception on Build {0} for Project {1}: {2}'.format(self.project_id,
                                                                          self.build_id,
                                                                          self.details)
