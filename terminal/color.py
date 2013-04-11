#!/usr/bin/env python
import os
import sys

codes = {}


def is_color_supported():
    "Find out if your terminal environment supports color."
    # shinx.util.console
    if not hasattr(sys.stdout, 'isatty'):
        return False
    if not sys.stdout.isatty():
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


class Color(object):
    def __init__(self, *items):
        self.items = items
        self.name = None
        self.fgcolor = None
        self.bgcolor = None

    def __str__(self):
        text = ''.join((unicode(item) for item in self.items))
        if not is_color_supported():
            return text

        if isinstance(self.fgcolor, int) and is_256color_supported():
            text = '\x1b[38;5;%im%s\x1b[0;39;49m' % (self.fgcolor, text)
        elif isinstance(self.fgcolor, str):
            code = codes.get(self.fgcolor, None)
            if code:
                text = '\x1b[%im%s\x1b[0;39;49m' % (code, text)

        if isinstance(self.bgcolor, int) and is_256color_supported():
            text = '\x1b[48;5;%im%s\x1b[0;39;49m' % (self.bgcolor, text)
        elif isinstance(self.bgcolor, str):
            code = codes.get(self.bgcolor, None)
            if code:
                text = '\x1b[%im%s\x1b[0;39;49m' % (code + 10, text)
        return text

    def __repr__(self):
        return repr(unicode(self))

    def __len__(self):
        return sum([len(item) for item in self.items])

    def __add__(self, s):
        if not isinstance(s, (basestring, Color)):
            msg = "Concatenatation failed: %r + %r (Not a ColorString or str)"
            raise TypeError(msg % (type(s), type(self)))
        return Color(self, s)

    def __radd__(self, s):
        if not isinstance(s, (basestring, Color)):
            msg = "Concatenatation failed: %r + %r (Not a ColorString or str)"
            raise TypeError(msg % (type(s), type(self)))
        return Color(s, self)


def colorize(name, text):
    if not is_color_supported():
        return text
    c = Color(text)
    if name.endswith('_bg'):
        c.bgcolor = name[:-3]
    else:
        c.fgcolor = name
    return c


def create_color_func(name):
    def inner(text):
        return colorize(name, text)
    globals()[name] = inner


_styles = [
    'bold', 'faint', 'italic', 'underline', 'blink',
    'overline', 'inverse', 'conceal', 'strike',
]
for i, _name in enumerate(_styles):
    codes[_name] = i + 1
    create_color_func(_name)


_colors = [
    'black', 'red', 'green', 'yellow', 'blue',
    'magenta', 'cyan', 'white'
]

for i, _name in enumerate(_colors):
    codes[_name] = 30 + i
    create_color_func(_name)
    create_color_func(_name + '_bg')


if __name__ == '__main__':
    for code in _colors:
        exec('print %s("%s")' % (code, code))
        exec('print %s_bg("%s")' % (code, code))

    for code in _styles:
        exec('print %s("%s")' % (code, code))
