# -*- coding: utf-8 -*-

from . import color
from .command import Command as _Command
from .log import Logger as _Logger


class Logger(_Logger):
    def message(self, level, *args):
        msg = ' '.join((str(o) for o in args))

        if level == 'start':
            return color.bold(msg)
        _ = {
            'debug': 'gray',
            'info': 'green',
            'warn': 'yellow',
            'error': 'red',
            'end': 'white',
        }

        if level == 'error':
            msg = color.red(msg)

        if level in _:
            fn = getattr(color, _[level])
            return '%s %s' % (fn('*'), msg)
        return msg


log = Logger()


class Command(_Command):
    def print_title(self, title):
        if 'Option' in title:
            print(color.green(title))
        elif 'Command' in title:
            print(color.magenta(title))
        else:
            print(title)
        return self

    def add_log_options(self, verbose_func=None, quiet_func=None):
        """
        A helper for setting up log options
        """

        if not verbose_func:
            def verbose_func():
                return log.config(verbose=True)

        if not quiet_func:
            def quiet_func():
                return log.config(quiet=True)

        self.option('-v, --verbose', 'show more logs', verbose_func)
        self.option('-q, --quiet', 'show less logs', quiet_func)
        return self
