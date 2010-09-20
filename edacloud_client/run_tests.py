#!/usr/bin/env python

try:
    import unittest2 as unittest
except ImportError:
    import unittest
import os
import coverage
from distutils.sysconfig import get_python_lib

site_packages_path = get_python_lib()

if __name__ == '__main__':
    cwd = os.getcwd()
    suite = unittest.defaultTestLoader.discover(start_dir=cwd)
    cov = coverage.coverage()
    cov.start()
    unittest.TextTestRunner().run(suite)
    cov.stop()
    cov.report(include=[os.path.join( cwd, 'edacloud_client', '*')])
