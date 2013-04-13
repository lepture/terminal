# coding: utf-8

import terminal


class MyCommand(terminal.Command):

    def print_title(self, title):
        if 'Option' in title:
            print(terminal.magenta(title))
        elif 'Command' in title:
            print(terminal.green(title))
        return self


program = MyCommand('terminal')

# add actions

subcommand = terminal.Command('sub')
program.action(subcommand)


@program.action
def log(verbose=False):
    """
    print a log test

    :param verbose: show more logs
    """

    terminal.log.config(verbose=verbose)
    terminal.log.info('this is a info message')
    terminal.log.verbose.info('this is a verbose message')


# add options
program.option('-f, --force', 'force to do something')
program.option('-o, --output <output>', 'output directory')

program.parse()

if program.output:
    print('output is %s' % program.output)
