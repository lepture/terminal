# -*- coding: utf-8 -*-

from . import color
from .command import Command as _Command
from .log import Logger as _Logger


class Command(_Command):
    def print_title(self, title):
        if 'Option' in title:
            print(color.green(title))
        elif 'Command' in title:
            print(color.magenta(title))
        else:
            print(title)
        return self


class Logger(_Logger):
    def message(self, level, *args):
        msg = ' '.join(args)

        if level == 'start':
            return color.bold(msg)
        _ = {
            'debug': 'gray',
            'info': 'green',
            'warn': 'yellow',
            'error': 'red',
            'end': 'white',
        }
        if level in _:
            fn = getattr(color, _[level])
            return '%s %s' % (fn('*'), msg)
        return msg


log = Logger()
