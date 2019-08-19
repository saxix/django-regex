#!/usr/bin/env python
import ast
import codecs
import os

import re
from setuptools import find_packages, setup

ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__)))
init = os.path.join(ROOT, 'src', 'django_regex', '__init__.py')

_version_re = re.compile(r'__version__\s+=\s+(.*)')
_name_re = re.compile(r'NAME\s+=\s+(.*)')

with open(init, 'rb') as f:
    content = f.read().decode('utf-8')
    version = str(ast.literal_eval(_version_re.search(content).group(1)))
    name = str(ast.literal_eval(_name_re.search(content).group(1)))


def read(*parts):
    here = os.path.abspath(os.path.dirname(__file__))
    return codecs.open(os.path.join(here, *parts)).read()


tests_requires = read('src/requirements/testing.pip')
install_requires = read('src/requirements/install.pip')
dev_requires = read('src/requirements/develop.pip')

setup(
    name=name,
    version=version,
    url='https://github.com/saxix/django-regex',
    author='Stefano Apostolico',
    author_email='s.apostolico@gmail.com',
    license="MIT",
    description='Fields and utilities to work with regular expression in Django',
    long_description=codecs.open('README.rst').read(),
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    install_requires=install_requires,
    tests_require=tests_requires,
    extras_require={
        'dev': dev_requires,
        'tests': tests_requires,
        'test': tests_requires,
        'extra': ['admin-extra-urls', ]
    },
    platforms=['linux'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Developers'
    ]
)
