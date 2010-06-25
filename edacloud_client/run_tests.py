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
    suite = unittest.defaultTestLoader.discover(start_dir=os.getcwd())
    cov = coverage.coverage()
    cov.start()
    unittest.TextTestRunner(verbosity=2).run(suite)
    cov.stop()
    #cov.report(omit_prefixes=[site_packages_path])
