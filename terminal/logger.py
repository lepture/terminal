#!/usr/bin/env python

import sys
import logging


class Logger(object):
    def __init__(self, name=None, level='notset', level_colors=None,
                 icon='|_', fill='  ', progress_func=None):
        self._depth = 0
        self._icon = icon
        self._fill = fill

        self._logger = logging.getLogger(name)
        self._logger.setLevel(getattr(logging, level.upper()))
        channel = logging.StreamHandler()
        channel.setFormatter(_LogFormatter())
        self._logger.addHandler(channel)

        self._level_colors = level_colors or {}
        self._progress_func = progress_func

    @property
    def icon(self):
        if not self._depth:
            return ''
        return self._fill * self._depth + self._icon

    def set_level(self, level):
        self._logger.setLevel(getattr(logging, level.upper()))

    def set_progress_func(self, func):
        self._progress_func = func

    def start(self, *args):
        if args:
            text = '%s%s' % (self._depth * self._fill, ' '.join(args))
            self.emit(text)

        self._depth += 1

    def end(self, *args):
        if self._depth == 0:
            #TODO exception
            raise Exception('')
        if args:
            text = '%s%s' % (self._depth * self._fill, ' '.join(args))
            self.emit(text)

        self._depth -= 1

    def debug(self, *args):
        text = '%s %s' % (self.icon, self._colorize('debug', *args))
        self._logger.debug(text)

    def info(self, *args):
        text = '%s %s' % (self.icon, self._colorize('info', *args))
        self._logger.info(text)

    def warn(self, *args):
        text = '%s %s' % (self.icon, self._colorize('warn', *args))
        self._logger.warn(text)

    def error(self, *args):
        text = '%s %s' % (self.icon, self._colorize('error', *args))
        self._logger.error(text)

    def emit(self, text, newline=True):
        if newline:
            sys.stdout.write(text + '\n')
        else:
            sys.stdout.write(text + '\r')
        sys.stdout.flush()

    def progress(self, current, total, end=False):
        status = '%s/%s' % (current, total)
        if self._progress_func:
            text = self._progress_func(
                current, total,
                blank=' ' * len(self.icon),
                status=' %s' % status)
        else:
            text = status
        if current < total and not end:
            self.emit(text, newline=False)
        else:
            self.emit(text, newline=True)

    def _colorize(self, name, *args):
        if not args:
            return ''
        text = ' '.join(args)
        func = self._level_colors.get(name)
        if not func:
            return text
        return func(text)


class _LogFormatter(logging.Formatter):
    def format(self, record):
        try:
            return record.getMessage()
        except Exception as e:
            return "Bad message (%r): %r" % (e, record.__dict__)
