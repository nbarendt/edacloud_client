from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='edacloud_client',
      version=version,
      description="EDA Cloud CmdLine Client",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Nick Barendt',
      author_email='',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
	"coverage==3.4b1",
	"mock==0.7.0b2",
	"unittest2==0.5.1",
	"distribute>=0.6.10",
      ],
      entry_points={
	'console_scripts' : [
		'cli = edacloud_client.cli:main',
	]
      },
      )
