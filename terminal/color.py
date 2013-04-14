# -*- coding: utf-8 -*-
import os
import sys

# Python 3
if sys.version_info[0] == 3:
    string_type = str
else:
    string_type = basestring


def is_color_supported():
    "Find out if your terminal environment supports color."
    # shinx.util.console
    if not hasattr(sys.stdout, 'isatty'):
        return False

    if not sys.stdout.isatty():
        return False

    if sys.platform == 'win32':
        try:
            import colorama
            colorama.init()
            return True
        except ImportError:
            return False

    if 'COLORTERM' in os.environ:
        return True

    term = os.environ.get('TERM', 'dumb').lower()
    return term in ('xterm', 'linux') or 'color' in term


def is_256color_supported():
    if not is_color_supported():
        return False
    term = os.environ.get('TERM', 'dumb').lower()
    return '256' in term


_reset = '\x1b[0;39;49m'


class Color(object):
    def __init__(self, *items):
        self.items = items

        self.styles = []
        self.fgcolor = None
        self.bgcolor = None

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        text = ''.join(unicode(item) for item in self.items)
        if not is_color_supported():
            return text

        is256 = is_256color_supported()
        if is256:
            if self.fgcolor is not None:
                text = '\x1b[38;5;%im%s%s' % (self.fgcolor, text, _reset)
            if self.bgcolor is not None:
                text = '\x1b[48;5;%im%s%s' % (self.bgcolor, text, _reset)

        else:
            if self.fgcolor is not None and self.fgcolor < 8:
                text = '\x1b[%im%s%s' % (30 + self.fgcolor, text, _reset)
            if self.bgcolor is not None and self.bgcolor < 8:
                text = '\x1b[%im%s%s' % (40 + self.bgcolor, text, _reset)

        if self.styles:
            code = ';'.join(str(i) for i in self.styles)
            text = '\x1b[%sm%s%s' % (code, text, _reset)

        return text

    def __repr__(self):
        return repr(unicode(self))

    def __len__(self):
        return sum([len(item) for item in self.items])

    def __add__(self, s):
        if not isinstance(s, (string_type, Color)):
            msg = "Concatenatation failed: %r + %r (Not a ColorString or str)"
            raise TypeError(msg % (type(s), type(self)))
        return Color(self, s)

    def __radd__(self, s):
        if not isinstance(s, (string_type, Color)):
            msg = "Concatenatation failed: %r + %r (Not a ColorString or str)"
            raise TypeError(msg % (type(s), type(self)))
        return Color(s, self)


def _create_color_func(name, fgcolor=None, bgcolor=None, *styles):
    def inner(text):
        c = Color(text)
        c.fgcolor = fgcolor
        c.bgcolor = bgcolor
        c.styles = styles
        return c
    globals()[name] = inner


_styles = (
    'bold', 'faint', 'italic', 'underline', 'blink',
    'overline', 'inverse', 'conceal', 'strike',
)

for i, _name in enumerate(_styles):
    _create_color_func(_name, None, None, i + 1)


_colors = (
    'black', 'red', 'green', 'yellow', 'blue',
    'magenta', 'cyan', 'white'
)

for i, _name in enumerate(_colors):
    _create_color_func(_name, fgcolor=i)
    _create_color_func(_name + '_bg', bgcolor=i)


for _name in ('grey', 'gray'):
    if is_256color_supported():
        _create_color_func(_name, fgcolor=8)
        _create_color_func(_name + '_bg', bgcolor=8)
    else:
        _create_color_func(_name, 0, None, 1)
        _create_color_func(_name + '_bg', None, 0, 1)


if __name__ == '__main__':
    for code in _colors:
        exec('print %s("%s")' % (code, code))
        exec('print %s_bg("%s")' % (code, code))

    for code in ('grey', 'gray'):
        exec('print %s("%s")' % (code, code))
        exec('print %s_bg("%s")' % (code, code))

    for code in _styles:
        exec('print %s("%s")' % (code, code))
