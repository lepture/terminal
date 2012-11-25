#!/usr/bin/env python

from .color import *
from .logger import Logger


logging = Logger(
    level_colors={
        'debug': lambda s: bold(black(s)),
        'info': green,
        'warn': yellow,
        'error': red,
    },
    icon=cyan('|_'),
)
