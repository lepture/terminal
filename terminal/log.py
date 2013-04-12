# -*- coding: utf-8 -*-
import sys
import copy


class Logger(object):
    def __init__(self, **kwargs):
        self.config(**kwargs)

    def config(self, **kwargs):
        self._is_verbose = False
        self._indent = kwargs.get('indent', 0)
        self._enable_verbose = kwargs.get('verbose', False)
        self._enable_quiet = kwargs.get('quiet', False)

    def message(self, level, *args):
        # rewrite this method to format your own message
        from . import color
        msg = ' '.join(args)
        if level == 'start':
            return color.magenta('=> ') + msg
        if level == 'end':
            return color.magenta('* ') + msg
        m = {
            'debug': 'gray',
            'info': 'green',
            'warn': 'yellow',
            'error': 'red'
        }
        if level in m:
            fn = getattr(color, m[level])
            return '%s: %s' % (fn(level), msg)
        return msg

    def writeln(self, level='info', *args):
        if not self._enable_verbose and self._is_verbose:
            return self
        msg = self.message(level, *args)
        if self._indent:
            msg = '  ' * self._indent + msg
        if level == 'error':
            sys.stderr.write(msg + '\n')
        else:
            sys.stdout.write(msg + '\n')
        return self

    @property
    def verbose(self):
        log = copy.copy(self)
        log._is_verbose = True
        return log

    def start(self, *args):
        self.writeln('start', *args)
        self._indent += 1
        return self

    def end(self, *args):
        self._indent -= 1
        return self.writeln('end', *args)

    def debug(self, *args):
        if self._enable_quiet:
            return self
        return self.writeln('debug', *args)

    def info(self, *args):
        if self._enable_quiet:
            return self
        return self.writeln('info', *args)

    def warn(self, *args):
        return self.writeln('warn', *args)

    def error(self, *args):
        return self.writeln('error', *args)
