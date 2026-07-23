import setuptools
from setuptools import dist
from setuptools import version
from setuptools import config
from setuptools import errors
from setuptools.dist import Distribution
from setuptools.config import setupcfg
from setuptools.config import pyprojecttoml
from setuptools.command import install
from setuptools.command import build
from setuptools.command import sdist
from setuptools.extern import packaging

def lambda_handler(event, context):
    name = event.get('name', 'my-package')
    version_str = event.get('version', '1.0.0')
    d = Distribution({
        'name': name,
        'version': version_str,
        'packages': ['mypackage']
    })
    return {
        'statusCode': 200,
        'body': {
            'name': d.get_name(),
            'version': d.get_version(),
            'packages': d.packages
        }
    }
