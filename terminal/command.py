# -*- coding: utf-8 -*-

import re
import sys
import inspect
from collections import OrderedDict


class Command(object):
    """
    The command interface.

    Create a :class:`Command` instance in your cli file::

        from terminal import Command
        app = Command('name', 'description', 'version')

    The command will add a default help option. If you set a version
    parameter, it will add a default version option too. You can add
    more options::

        app.option('-v, --verbose', 'show more logs')
        app.option('-o, --output <output>', 'the output file')

    Usually you will need a subcommand feature, add a subcommand like
    this::

        subcommand = Command('build', 'build command')
        subcommand.option('--source <source>', 'source directory')

        app.action(subcommand)

    A subcommand is a full featured Command, which means you can add
    a subcommand to the subcommand too. We can add a subcommand with
    the decorator feature::

        @app
        def build(source='.'):
            '''
            generate the documentation.

            :param source: the source directory
            '''
            pass

    After defining the command, we can parse the command line argv::

        app.parse()

    If we have pased ``--verbose`` in the terminal, we can get::

        assert app.verbose is True


    :param name: program name
    :param description: description of the program
    :param version: version of the program
    :param usage: usage of the program
    """

    def __init__(self, name, description=None, version=None, usage=None):
        self._name = name
        self._description = description
        self._version = version
        self._usage = usage

        self._default_func = None
        self._option_list = []
        self._command_list = []

        self._results = OrderedDict()
        self._rests = []

        self.add_default_options()

    def __getitem__(self, key):
        return self._results.get(key)

    def __getattr__(self, key):
        try:
            return super(Command, self).__getattr__(key)
        except AttributeError:
            return self._results.get(key)

    def __call__(self, func):
        """
        Decorator for add action.

        Example as decorator::

            @command
            def foo(port=5000):
                '''
                docstring as the description

                :param port: description of port
                '''
                # server(port)

        """
        doclines = func.__doc__.splitlines()
        doclines = filter(lambda o: o.strip(), doclines)
        doclines = map(lambda o: o.strip(), doclines)

        def find_description(arg):
            text = ':param %s:' % arg
            for line in doclines:
                if line.startswith(text):
                    return line.replace(text, '').strip()
            return None

        desc = None
        if doclines:
            desc = doclines[0]

        cmd = Command(func.__name__, desc)

        args, varargs, keywords, defaults = inspect.getargspec(func)

        defaults = defaults or []
        kwargs = dict(zip(*[reversed(i) for i in (args, defaults)]))

        for arg in args:
            desc = find_description(arg)
            if arg in kwargs:
                value = kwargs[arg]
                if value is True:
                    cmd.option('--no-%s' % arg, desc)
                elif value is False:
                    cmd.option('-%s, --%s' % (arg[0], arg), desc)
                else:
                    cmd.option('-%s, --%s <%s>' % (arg[0], arg, arg), desc)
            else:
                cmd.option('-%s, --%s <%s>' % (arg[0], arg, arg), desc)

        cmd._default_func = func
        self.action(cmd)
        return func

    @property
    def args(self):
        return self._rests

    def get(self, key):
        """
        Get parsed result.
        """
        return self._results.get(key)

    def option(self, name, description=None, action=None):
        """
        Add or get option.

        Here are some examples::

            command.option('-v, --verbose', 'show more log')
            command.option('--tag <tag>', 'tag of the package')
            command.option('-s, --source <source>', 'the source repo')

        :param name: arguments of the option
        :param description: description of the option
        :param action: a function to be invoked

        """
        self._option_list.append((name, description, action))
        return self

    def add_default_options(self):
        self.option(
            '-h, --help',
            'output the help menu',
            self.print_help
        )
        if self._version:
            self.option(
                '-V, --version',
                'output the version number',
                self.print_version
            )
        return self

    def parse_options(self, arg):
        """
        Parse options with the argv

        :param arg: one arg from argv
        """

        if not arg.startswith('-'):
            return False

        value = None
        if '=' in arg:
            arg, value = arg.split('=')

        regex = re.compile(r'(-\w)?(?:\,\s*)?(--[\w\-]+)?(\s+<.*>)?')
        for option in self._option_list:
            name = option[0].strip()
            m = regex.findall(name)
            if not m:
                raise RuntimeError('Invalid Option: %s', name)

            shortname, longname, tag = m[0]

            if arg not in (shortname, longname):
                continue

            action = option[2]
            if action:
                action()
                return sys.exit(0)

            if not tag and not longname:
                self._results[shortname] = True
                return True

            if not tag and longname.startswith('--no-'):
                self._results[longname[5:]] = False
                return True

            if not tag:
                self._results[longname[2:]] = True
                return True

            # has tag, it should has value
            if not value:
                if self._args:
                    value = self._args[0]
                    self._args = self._args[1:]

            tag = tag.strip()
            self._results[tag[1:-1]] = value
            return True

        return False

    def action(self, command):
        """
        Add a subcommand.

        :param command: a function or a Command
        """
        self._command_list.append(command)
        return self

    def parse(self, argv=None):
        """
        Parse argv of terminal

        :param argv: default is sys.argv
        """
        if not argv:
            argv = sys.argv

        self._args = argv[1:]
        if not self._args:
            return self

        cmd = self._args[0]

        if not cmd.startswith('-'):
            # parse subcommands
            for command in self._command_list:
                if isinstance(command, Command) and command._name == cmd:
                    return command.parse(self._args)

                if inspect.isfunction(command) and command.__name__ == cmd:
                    return command()

        while self._args:
            arg = self._args[0]
            self._args = self._args[1:]
            if not self.parse_options(arg):
                self._rests.append(arg)

        if self._default_func:
            self._default_func(**self._results)
        return self

    def print_version(self):
        print('  %s %s' % (self._name, self._version or ''))
        return self

    def print_title(self, title):
        print(title)
        return self

    def print_help(self):
        print('')
        self.print_version()

        if self._usage:
            print('\n  %s' % self._usage)
        else:
            if self._command_list:
                usage = 'Usage: %s <command> [option]' % self._name
            else:
                usage = 'Usage: %s [option]' % self._name
            print('\n  %s' % usage)

        arglen = max(len(name) for name, desc, action in self._option_list)
        arglen += 2

        self.print_title('\n  Options:\n')
        for name, desc, action in self._option_list:
            print('    %s %s' % (_pad(name, arglen), desc or ''))
        print('')

        if not self._command_list:
            return sys.exit(0)

        self.print_title('\n  Commands:\n')
        for cmd in self._command_list:
            if isinstance(cmd, Command):
                name = _pad(cmd._name, arglen)
                desc = cmd._description or ''
                print('    %s %s' % (_pad(name, arglen), desc))
            elif inspect.isfunction(cmd):
                name = _pad(cmd.__name__, arglen)
                desc = cmd.__doc__
                print('    %s %s' % (_pad(name, arglen), desc))

        print('')
        return sys.exit(0)


def _pad(msg, length):
    return '%s%s' % (msg, ' ' * (length - len(msg)))
