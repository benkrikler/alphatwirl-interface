#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""
from setuptools import setup, find_packages


# with open('README.rst') as readme_file:
#     readme = readme_file.read()
#
# with open('HISTORY.rst') as history_file:
#     history = history_file.read()
#
# long_description = readme + '\n\n' + history
long_description = 'Interface development package for alphatwirl'

authors = []
author_emails = []
with open('authors.txt') as f:
    for line in f.readlines():
        author, email = line.split(',')
        authors.append(author)
        author_emails.append(email)
authors = ', '.join(authors)
author_emails = ', '.join(author_emails)

install_reqs = [
    'alphatwirl',
    'numpy',
]

setup_requirements = [
    'pytest-runner',
    # TODO(kreczko): put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    'flake8',
    'pytest',
    # TODO: put package test requirements here
]

setup(
    name='alphatwirl_interface',
    version='0.0.1',
    description="Interface development package for alphatwirl",
    long_description=long_description,
    author=authors,
    author_email=author_emails,
    url='https://github.com/alphatwirl/alphatwirl-interface',
    packages=find_packages(include=['alphatwirl_interface']),
    include_package_data=True,
    install_requires=install_reqs,
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords='alphatwirl_interface',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='test',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
