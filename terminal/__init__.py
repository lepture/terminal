#!/usr/bin/env python

from .color import *
from .logger import Logger
from .progress import Progress


logging = Logger(
    level_colors={
        'debug': lambda s: bold(black(s)),
        'info': green,
        'warn': yellow,
        'error': red,
    },
    icon=cyan('|_'),
    progress_func=Progress(marker='-', right='>')
)
