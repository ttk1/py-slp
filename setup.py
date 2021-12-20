#!/usr/bin/env python

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

entry_points = {
    'console_scripts': [
        'server-list-ping = slp.server_list_ping:main'
    ]
}

setup(
    name='py-slp',
    version='1.0.0',
    description='Python implementation of Server List Ping.',
    long_description=readme,
    author='tama@ttk1.net',
    author_email='tama@ttk1.net',
    url='https://github.com/ttk1/py-slp',
    license=license,
    packages=find_packages(exclude=('test',)),
    entry_points=entry_points
)
