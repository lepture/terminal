# -*- coding: utf-8 -*-
"""
    terminal.color
    ~~~~~~~~~~~~~~

    ANSI color control for terminal.

    :copyright: (c) 2013 by Hsiaoming Yang.
"""

# http://en.wikipedia.org/wiki/ANSI_escape_code
# http://en.wikipedia.org/wiki/Web_colors
# https://gist.github.com/MicahElliott/719710

import os
import sys

# Python 3
if sys.version_info[0] == 3:
    string_type = str
    unicode = str
else:
    string_type = (unicode, str)


def is_color_supported():
    "Find out if your terminal environment supports color."
    # shinx.util.console
    if not hasattr(sys.stdout, 'isatty'):
        return False

    if not sys.stdout.isatty() and 'TERMINAL-COLOR' not in os.environ:
        return False

    if sys.platform == 'win32':  # pragma: no cover
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
    "Find out if your terminal environment supports 256 color."
    if not is_color_supported():
        return False
    term = os.environ.get('TERM', 'dumb').lower()
    return '256' in term


def rgb2ansi(r, g, b):
    """
    Convert an RGB color to 256 ansi graphics.
    """

    # Thanks to
    # https://github.com/tehmaze/ansi/blob/master/ansi/colour/rgb.py

    grayscale = False
    poss = True
    step = 2.5

    while poss:
        if min(r, g, b) < step:
            grayscale = max(r, g, b) < step
            poss = False

        step += 42.5

    if grayscale:
        return 232 + int(float(sum((r, g, b)) / 33.0))

    m = ((r, 36), (g, 6), (b, 1))
    return 16 + sum(int(6 * float(val) / 256) * mod for val, mod in m)


def hex2ansi(code):
    """
    Convert hex code to ansi.
    """

    if code.startswith('#'):
        code = code[1:]

    if len(code) == 3:
        # efc -> eeffcc
        return rgb2ansi(*map(lambda o: int(o * 2, 16), code))

    if len(code) != 6:
        raise ValueError('invalid color code')

    rgb = (code[:2], code[2:4], code[4:])
    return rgb2ansi(*map(lambda o: int(o, 16), rgb))


_reset = '\x1b[0;39;49m'
_styles = (
    'bold', 'faint', 'italic', 'underline', 'blink',
    'overline', 'inverse', 'conceal', 'strike',
)
_colors = (
    'black', 'red', 'green', 'yellow', 'blue',
    'magenta', 'cyan', 'white'
)


def _color2ansi(color):
    if color in _colors:
        return _colors.index(color)

    if isinstance(color, string_type):
        return hex2ansi(color)
    elif isinstance(color, (tuple, list)):
        return rgb2ansi(*color)

    raise ValueError('invalid color: %s' % color)


class Color(object):
    """
    Color object for painters.

    You should always use the high-level API of colors and styles,
    such as :class:`red` and :class:`bold`.

    But if you are so interested in this module, you are welcome to
    use some advanced features::

        s = Color('text')
        print(s.bold.red.italic)

    All ANSI colors and styles are available on Color.
    """

    def __init__(self, *items):
        self.items = items

        self.styles = []
        self.fgcolor = None
        self.bgcolor = None

    def __getattr__(self, key):
        if key.endswith('_bg'):
            name = key[:-3]
            if name not in _colors:
                raise AttributeError("Color has no attribute '%s'" % key)
            self.bgcolor = _colors.index(name)
            return self

        if key in _colors:
            self.fgcolor = _colors.index(key)
            return self

        if key in _styles:
            code = _styles.index(key)
            self.styles.append(code + 1)
            return self
        try:
            return object.__getattribute__(self, key)
        except AttributeError:
            raise AttributeError("Color has no attribute '%s'" % key)

    def __str__(self):
        text = ''.join(unicode(item) for item in self.items)

        if unicode != str:
            text = text.encode('utf-8')

        if not is_color_supported():
            return text

        is256 = is_256color_supported()

        if self.fgcolor and not isinstance(self.fgcolor, int):
            self.fgcolor = _color2ansi(self.fgcolor)

        if self.bgcolor and not isinstance(self.bgcolor, int):
            self.bgcolor = _color2ansi(self.bgcolor)

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
        return repr(str(self))

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


def colorize(text, color, background=False):
    """
    Colorize text with hex code.

    :param text: the text you want to paint
    :param color: a hex color or rgb color
    :param background: decide to colorize background

    ::

        colorize('hello', 'ff0000')
        colorize('hello', '#ff0000')
        colorize('hello', (255, 0, 0))

    """

    if color in _styles:
        c = Color(text)
        c.styles = [_styles.index(color) + 1]
        return c

    c = Color(text)
    if background:
        c.bgcolor = _color2ansi(color)
    else:
        c.fgcolor = _color2ansi(color)
    return c


def _create_color_func(text, fgcolor=None, bgcolor=None, *styles):
    c = Color(text)
    c.fgcolor = fgcolor
    c.bgcolor = bgcolor
    c.styles = styles
    return c


def bold(text):
    """
    Bold style.
    """
    return _create_color_func(text, None, None, 1)


def faint(text):
    """
    Faint style.
    """
    return _create_color_func(text, None, None, 2)


def italic(text):
    """
    Italic style.
    """
    return _create_color_func(text, None, None, 3)


def underline(text):
    """
    Underline style.
    """
    return _create_color_func(text, None, None, 4)


def blink(text):
    """
    Blink style.
    """
    return _create_color_func(text, None, None, 5)


def overline(text):
    """
    Overline style.
    """
    return _create_color_func(text, None, None, 6)


def inverse(text):
    """
    Inverse style.
    """
    return _create_color_func(text, None, None, 7)


def conceal(text):
    """
    Conceal style.
    """
    return _create_color_func(text, None, None, 8)


def strike(text):
    """
    Strike style.
    """
    return _create_color_func(text, None, None, 9)


def black(text):
    """
    Black color.
    """
    return _create_color_func(text, fgcolor=0)


def red(text):
    """
    Red color.
    """
    return _create_color_func(text, fgcolor=1)


def green(text):
    """
    Green color.
    """
    return _create_color_func(text, fgcolor=2)


def yellow(text):
    """
    Yellow color.
    """
    return _create_color_func(text, fgcolor=3)


def blue(text):
    """
    Blue color.
    """
    return _create_color_func(text, fgcolor=4)


def magenta(text):
    """
    Magenta color.
    """
    return _create_color_func(text, fgcolor=5)


def cyan(text):
    """
    Cyan color.
    """
    return _create_color_func(text, fgcolor=6)


def white(text):
    """
    White color.
    """
    return _create_color_func(text, fgcolor=7)


def gray(text):
    """
    Gray color.
    """
    if is_256color_supported():
        return _create_color_func(text, fgcolor=8)
    return _create_color_func(text, 0, None, 8)


def grey(text):
    """
    Alias of gray.
    """
    return gray(text)


def black_bg(text):
    """
    Black background.
    """
    return _create_color_func(text, bgcolor=0)


def red_bg(text):
    """
    Red background.
    """
    return _create_color_func(text, bgcolor=1)


def green_bg(text):
    """
    Green background.
    """
    return _create_color_func(text, bgcolor=2)


def yellow_bg(text):
    """
    Yellow background.
    """
    return _create_color_func(text, bgcolor=3)


def blue_bg(text):
    """
    Blue background.
    """
    return _create_color_func(text, bgcolor=4)


def magenta_bg(text):
    """
    Magenta background.
    """
    return _create_color_func(text, bgcolor=5)


def cyan_bg(text):
    """
    Cyan background.
    """
    return _create_color_func(text, bgcolor=6)


def white_bg(text):
    """
    White background.
    """
    return _create_color_func(text, bgcolor=7)


def gray_bg(text):
    """
    Gray background.
    """
    if is_256color_supported():
        return _create_color_func(text, bgcolor=8)
    return _create_color_func(text, None, 0, 1)


def grey_bg(text):
    """
    Alias of gray_bg.
    """
    return gray_bg(text)
