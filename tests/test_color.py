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


class TestColor(object):
    def test_property(self):
        s = terminal.Color('text')
        print(s.bold.red.underline)
        print(s.green_bg)

        s = terminal.Color('text')
        s.bgcolor = 'red'
        print(s)

        s.bgcolor = 'd64'
        print(s)

    @raises(AttributeError)
    def test_property_raise(self):
        s = terminal.Color('text')
        print(s.unknown)

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
