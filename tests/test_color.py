import terminal


def test_colorize():
    print(terminal.colorize('foo', 'red'))
    print(terminal.colorize('foo', '#ff0000'))
    print(terminal.colorize('foo', 'ff0000'))
    print(terminal.colorize('foo', (255, 0, 0)))


def test_colors():
    print(terminal.cyan('cyan color'))
    print(terminal.blue('blue color'))
    print(terminal.yellow('yellow color'))
    print(terminal.magenta('magenta color'))
    print(terminal.red(terminal.green('green color')))


def test_styles():
    print(terminal.bold('bold style'))
    print(terminal.bold(terminal.underline('bold and underline style')))


def test_color():
    c = terminal.Color('text')
    print(c.bold.red.underline)
