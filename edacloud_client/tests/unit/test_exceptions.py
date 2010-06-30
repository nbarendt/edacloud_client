from edacloud_client.exceptions import *
from unittest2 import TestCase

class UnsupportedURLSchemeTestCase(TestCase):
    bad_scheme = 'badscheme'
    def setUp(self):
        self.exc = UnsupportedURLScheme(self.bad_scheme)
        
    def test_CanCreate(self):
        self.assertEqual(self.bad_scheme, self.exc.scheme)

    def test_CanGetStringRepresentation(self):
        self.assertEqual('Unsupported Scheme: {0}'.format(self.bad_scheme), str(self.exc))

class HTTPErrorTestCase(TestCase):
    status = 500
    reason = 'forced server error'
    def setUp(self):
        self.exc = HTTPError(self.status, self.reason)
        
    def test_CanCreate(self):
        self.assertEqual(self.status, self.exc.status)
        self.assertEqual(self.reason, self.exc.reason)

    def test_CanGetStringRepresentation(self):
        self.assertEqual('HTTP Server Returned {0} : {1}'.format(self.status, self.reason), str(self.exc))

class BadProjectIDTestCase(TestCase):
    bad_id = '1'
    id_exc_class = BadProjectID
    id_type = 'Project'
    def setUp(self):
        self.exc = self.id_exc_class(self.bad_id)

    def test_CanCreate(self):
        self.assertEqual(self.bad_id, self.exc.id)

    def test_CanGetStringRepresentation(self):
        self.assertEqual('Bad {0} ID: {1}'.format(self.id_type, self.bad_id), str(self.exc))

class BadBuildIDTestCase(TestCase):
    id_exc_class = BadBuildID
    id_type = 'Build'

class BuildExceptionTestCase(TestCase):
    project_id = 'a'
    build_id = 'b'
    details = 'forced build error'
    def setUp(self):
        self.exc = BuildException(self.project_id, self.build_id, self.details)

    def test_CanCreate(self):
        self.assertEqual(self.project_id, self.exc.project_id)
        self.assertEqual(self.build_id, self.exc.build_id)
        self.assertEqual(self.details, self.exc.details)

    def test_CanGetStringRepresentation(self):
        self.assertEqual('Build Exception on Build {0} for Project {1}: {2}'.format(
            self.project_id,
            self.build_id,
            self.details),
                         str(self.exc))
