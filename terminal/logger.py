#!/usr/bin/env python

import os
import sys
import logging


class Logger(object):
    def __init__(self, name=None, level='notset', icon='|_', fill='  ',
                 progress=None, formatter=None):
        self._depth = 0
        self._icon = icon
        self._fill = fill

        self._logger = logging.getLogger(name)
        self.set_level(level)
        if formatter:
            self.format_logger(formatter)

        if progress:
            self._progress = progress
        else:
            self._progress = Progress()

    @property
    def prefix(self):
        if not self._depth:
            return ''
        return self._fill * self._depth + self._icon

    def format_logger(self, formatter):
        "Subclass can rewrite this function."
        channel = logging.StreamHandler()
        channel.setFormatter(formatter)
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
        if self._progress:
            text = self._progress(
                current, total,
                blank=' ' * len(self.prefix),
                status=' %s' % status)
        else:
            text = status
        if current < total and not end:
            self.emit(text, newline=False)
        else:
            self.emit(text, newline=True)


class NestFormater(logging.Formatter):
    def __init__(self, handler, colors, *args, **kwargs):
        super(NestFormater, self).__init__(*args, **kwargs)
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


def get_terminal_width():
    """Borrowed from the py lib."""
    try:
        import termios
        import fcntl
        import struct
        call = fcntl.ioctl(0, termios.TIOCGWINSZ,
                           struct.pack('hhhh', 0, 0, 0, 0))
        height, width = struct.unpack('hhhh', call)[:2]
        terminal_width = width
    except (SystemExit, KeyboardInterrupt):
        raise
    except:
        # FALLBACK
        terminal_width = int(os.environ.get('COLUMNS', 80)) - 1
    return terminal_width


class Progress(object):
    def __init__(self, marker='#', left='', right='', fill=' '):
        self.marker = marker
        self.left = left
        self.right = right
        if len(fill) != 1:
            raise ValueError('You must a char.')
        self.fill = fill
        self.width = get_terminal_width()

    def __call__(self, current, total, blank='', status=''):
        if current > total:
            raise ValueError("current can't be larger than total.")
        count = len(blank) + len(status) + len(self.left) + len(self.right)

        marker = int((self.width - count) / float(total) * current) * \
                self.marker
        if len(marker) >= self.width - count:
            marker = marker[:self.width - count]

        bar = blank + self.left + marker + self.right
        text = status.rjust(self.width, self.fill)
        text = text.replace(self.fill * len(bar), bar, 1)
        return text
