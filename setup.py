#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
kwargs = {}
if sys.platform == 'win32':
    kwargs['install_requires'] = ['colorama']

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import terminal
from email.utils import parseaddr
author, author_email = parseaddr(terminal.__author__)

setup(
    name='terminal',
    version=terminal.__version__,
    author=author,
    author_email=author_email,
    url=terminal.__homepage__,
    packages=['terminal'],
    description=terminal.__doc__,
    long_description=open('README.rst').read(),
    license=open('LICENSE').read(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    **kwargs
)
