#!/usr/bin/env python

"""
A terminal environment tools.
"""

from __future__ import absolute_import

from .color import *
from .prompt import *
from .log import Logger
from .command import Command

log = Logger()

__homepage__ = 'http://lab.lepture.com/terminal/'
__author__ = 'Hsiaoming Yang <me@lepture.com>'
__version__ = '0.1.0a1'
