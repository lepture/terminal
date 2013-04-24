import os
import terminal
from nose.tools import raises


def test_colorize():
    print(terminal.colorize('bold', 'bold'))
    print(terminal.colorize('red', 'red'))
    print(terminal.colorize('red', '#ff0000'))
    print(terminal.colorize('red', 'ff0000'))
    print(terminal.colorize('red', 'f00'))
    print(terminal.colorize('red', (255, 0, 0)))
    print(terminal.colorize('gray', (80, 80, 80)))
    print(terminal.colorize('red', 'f00', True))


def test_colors():
    print(terminal.cyan('cyan color'))
    print(terminal.blue('blue color'))
    print(terminal.yellow('yellow color'))
    print(terminal.magenta('magenta color'))
    print(terminal.black('black color'))
    print(terminal.white('white color'))
    print(terminal.gray('gray color'))
    print(terminal.grey('grey color'))
    print(terminal.red(terminal.green('green color')))

    print(terminal.cyan_bg('cyan background'))
    print(terminal.blue_bg('blue background'))
    print(terminal.yellow_bg('yellow background'))
    print(terminal.magenta_bg('magenta background'))
    print(terminal.black_bg('black background'))
    print(terminal.white_bg('white background'))
    print(terminal.gray_bg('gray background'))
    print(terminal.grey_bg('grey background'))
    print(terminal.red_bg(terminal.green_bg('green background')))


def test_styles():
    print(terminal.bold('bold style'))
    print(terminal.faint('faint style'))
    print(terminal.italic('italic style'))
    print(terminal.underline('underline style'))
    print(terminal.blink('blink style'))
    print(terminal.overline('overline style'))
    print(terminal.inverse('inverse style'))
    print(terminal.conceal('conceal style'))
    print(terminal.strike('strike style'))
    print(terminal.bold(terminal.underline('bold and underline style')))


@raises(ValueError)
def test_hex2ansi():
    terminal.hex2ansi('ffbbccd')


@raises(ValueError)
def test_raise_colorize():
    print(terminal.colorize('text', {'foo': 'bar'}))


def test_256color():
    env = Environ()
    env.enable_256color()

    print(terminal.gray('gray color'))
    print(terminal.gray_bg('gray background'))

    env.reset()


class Environ(object):
    def __init__(self):
        self.term = os.environ.get('TERM', None)

    def enable_256color(self):
        os.environ['TERMINAL-TEST'] = 'true'
        os.environ['COLORTERM'] = 'true'
        os.environ['TERM'] = 'xterm-256color'

    def enable_color(self):
        os.environ['TERMINAL-TEST'] = 'true'
        os.environ['TERM'] = 'xterm'

    def reset(self):
        del os.environ['TERMINAL-TEST']
        if 'COLORTERM' in os.environ:
            del os.environ['COLORTERM']
        if self.term:
            os.environ['TERM'] = self.term


class TestColor(object):
    def test_property(self):
        env = Environ()
        env.enable_color()

        s = terminal.Color('text')
        print(s.bold.red.underline)
        print(s.green_bg)
        env.reset()

    def test_set_attribute(self):
        env = Environ()
        env.enable_256color()
        s = terminal.Color('text')
        s.bgcolor = 'red'
        s.fgcolor = 'white'
        print(s)

        s.bgcolor = 'd64'
        print(s)
        env.reset()

    @raises(AttributeError)
    def test_property_raise(self):
        s = terminal.Color('text')
        print(s.unknown)

    @raises(AttributeError)
    def test_unknown_bg(self):
        s = terminal.Color('text')
        print(s.unknown_bg)

    def test_plus(self):
        foo = terminal.Color('foo')
        print(foo.green + 'bar')
        print('bar' + foo)

        assert len(foo) == 3
        assert len('bar' + foo) == 6

        bar = terminal.Color('foo')
        print(foo.green + bar)
        print(bar + foo)

    @raises(TypeError)
    def test_add_raise(self):
        foo = terminal.Color('foo')
        print(foo.green + 1)

    @raises(TypeError)
    def test_radd_raise(self):
        foo = terminal.Color('foo')
        print(1 + foo.green)

    def test_repr(self):
        foo = terminal.Color('foo')
        foo.fgcolor = 'red'
        assert repr(foo) == repr(str(foo))
