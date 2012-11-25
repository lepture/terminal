#!/usr/bin/env python

from .color import *
from .logger import Logger


logging = Logger(
    level_colors={
        'debug': lightgray,
        'info': green,
        'warn': yellow,
        'error': red,
    },
    icon=darkgray('|_'),
)
