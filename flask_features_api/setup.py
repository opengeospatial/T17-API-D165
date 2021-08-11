# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "openapi_server"
VERSION = "1.0.0"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "connexion>=2.0.2",
    "swagger-ui-bundle>=0.0.2",
    "python_dateutil>=2.6.0"
]

setup(
    name=NAME,
    version=VERSION,
    description="A sample API conforming to the draft standard OGC API - Features - Part 1: Core",
    author_email="info@example.org",
    url="",
    keywords=["OpenAPI", "A sample API conforming to the draft standard OGC API - Features - Part 1: Core"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['openapi/openapi.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['openapi_server=openapi_server.__main__:main']},
    long_description="""\
    This is a sample OpenAPI definition that conforms to the conformance classes \&quot;Core\&quot;, \&quot;GeoJSON\&quot;, \&quot;HTML\&quot; and \&quot;OpenAPI 3.0\&quot; of the draft standard \&quot;OGC API - Features - Part 1: Core\&quot;.  This example is a generic OGC API Features definition that uses path parameters to describe all feature collections and all features. The generic OpenAPI definition does not provide any details on the collections or the feature content. This information is only available from accessing the feature collection resources.  There is [another example](ogcapi-features-1-example2.yaml) that specifies each collection explicitly.
    """
)

