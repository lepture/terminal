#!/usr/bin/env python

"""
A terminal environment tools.
"""


from .color import *
from .logger import Logger
from .progress import Progress


__author__ = 'Hsiaoming Yang <lepture@me.com>'
__version__ = '0.0.1'
__homepage__ = 'http://lab.lepture.com/terminal/'


logging = Logger(
    colors={
        'debug': grey,
        'info': green,
        'warn': yellow,
        'error': red,
    },
    icon=cyan('|-'),
    progress_func=Progress(marker='-', right='>')
)
