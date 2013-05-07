#!/usr/bin/env python
# flake8: noqa

"""
A terminal environment tools.
"""

from __future__ import absolute_import

from .color import *
from .prompt import *
from .log import Logger
from .command import Command, Option

log = Logger()

__homepage__ = 'https://github.com/lepture/terminal'
__author__ = 'Hsiaoming Yang <me@lepture.com>'
__version__ = '0.3.0'
