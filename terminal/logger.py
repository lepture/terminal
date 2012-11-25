#!/usr/bin/env python

import sys
import logging


class Logger(object):
    def __init__(self, name=None, level='notset',
                 level_colors=None, icon='|_'):
        self._depth = 0
        self._icon = icon

        self._logger = logging.getLogger(name)
        self._logger.setLevel(getattr(logging, level.upper()))
        channel = logging.StreamHandler()
        channel.setFormatter(_LogFormatter())
        self._logger.addHandler(channel)

        self._level_colors = level_colors or {}

    def set_level(self, level):
        self._logger.setLevel(getattr(logging, level.upper()))

    def start(self, *args):
        if args:
            text = '%s%s' % (self._depth * ' ', ' '.join(args))
            sys.stdout.write(text)
            sys.stdout.write('\n')
            sys.stdout.flush()

        self._depth += 1

    def end(self, *args):
        if self._depth == 0:
            #TODO exception
            raise Exception('')
        if not args:
            return
        self._depth -= 1
        text = '%s%s' % (self._depth * ' ', ' '.join(args))
        sys.stdout.write(text)
        sys.stdout.write('\n')
        sys.stdout.flush()

    @property
    def icon(self):
        if not self._depth:
            return ''
        return '%s%s ' % (' ' * self._depth, self._icon)

    def _colorize(self, name, *args):
        if not args:
            return ''
        text = ' '.join(args)
        func = self._level_colors.get(name)
        if not func:
            return text
        return func(text)

    def debug(self, *args):
        text = '%s%s' % (self.icon, self._colorize('debug', *args))
        self._logger.debug(text)

    def info(self, *args):
        text = '%s%s' % (self.icon, self._colorize('info', *args))
        self._logger.info(text)

    def warn(self, *args):
        text = '%s%s' % (self.icon, self._colorize('warn', *args))
        self._logger.warn(text)

    def error(self, *args):
        text = '%s%s' % (self.icon, self._colorize('error', *args))
        self._logger.error(text)


class _LogFormatter(logging.Formatter):
    def format(self, record):
        try:
            return record.getMessage()
        except Exception as e:
            return "Bad message (%r): %r" % (e, record.__dict__)
