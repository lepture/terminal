import terminal


def test_colorize():
    print(terminal.colorize('bold', 'bold'))
    print(terminal.colorize('red', 'red'))
    print(terminal.colorize('red', '#ff0000'))
    print(terminal.colorize('red', 'ff0000'))
    print(terminal.colorize('red', 'f00'))
    print(terminal.colorize('red', (255, 0, 0)))
    print(terminal.colorize('gray', (80, 80, 80)))


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

    def test_plus(self):
        foo = terminal.Color('foo')
        print(foo.green + 'bar')
        print('bar' + foo)

        bar = terminal.Color('foo')
        print(foo.green + bar)
        print(bar + foo)
