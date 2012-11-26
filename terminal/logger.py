#!/usr/bin/env python

import sys
import logging


class Logger(object):
    def __init__(self, name=None, level='notset', icon='|_', fill='  ',
                 progress_func=None, colors=None):
        self._depth = 0
        self._icon = icon
        self._fill = fill

        self._logger = logging.getLogger(name)
        self.set_level(level)
        self.format_logger(colors)
        self.progress_func = progress_func

    @property
    def prefix(self):
        if not self._depth:
            return ''
        return self._fill * self._depth + self._icon

    def format_logger(self, colors=None):
        "Subclass can rewrite this function."
        channel = logging.StreamHandler()
        channel.setFormatter(_NestFormater(self, colors))
        self._logger.addHandler(channel)

    def set_level(self, level):
        self._logger.setLevel(getattr(logging, level.upper()))

    def start(self, *args):
        if args:
            text = '%s%s' % (self._depth * self._fill, ' '.join(args))
            self.emit(text)

        self._depth += 1

    def end(self, *args):
        if self._depth == 0:
            raise RuntimeError('There is no nested logging.')
        if args:
            text = '%s%s' % (self._depth * self._fill, ' '.join(args))
            self.emit(text)

        self._depth -= 1

    def debug(self, *args):
        self._logger.debug(' '.join(args))

    def info(self, *args):
        self._logger.info(' '.join(args))

    def warn(self, *args):
        self._logger.warn(' '.join(args))

    def error(self, *args):
        self._logger.error(' '.join(args))

    def emit(self, text, newline=True):
        if newline:
            sys.stdout.write(text + '\n')
        else:
            sys.stdout.write(text + '\r')
        sys.stdout.flush()

    def progress(self, current, total, end=False):
        status = '%s/%s' % (current, total)
        if self.progress_func:
            text = self.progress_func(
                current, total,
                blank=' ' * len(self.prefix),
                status=' %s' % status)
        else:
            text = status
        if current < total and not end:
            self.emit(text, newline=False)
        else:
            self.emit(text, newline=True)


class _NestFormater(logging.Formatter):
    def __init__(self, handler, colors, *args, **kwargs):
        super(_NestFormater, self).__init__(*args, **kwargs)
        self._handler = handler
        self._colors = colors

    def format(self, record):
        try:
            message = record.getMessage()
        except Exception as e:
            message = "Bad message (%r): %r" % (e, record.__dict__)

        prefix = self._handler.prefix
        if 'module' in self._colors:
            module = ' (%(module)s:%(lineno)d)' % record.__dict__
            prefix = prefix + self._colorize('module', module)
        message = self._colorize(record.levelname.lower(), message)
        return prefix + ' ' + message

    def _colorize(self, name, *args):
        if not args:
            return ''
        text = ' '.join(args)
        func = self._colors.get(name)
        if not func:
            return text
        return func(text)
