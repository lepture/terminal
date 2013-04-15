# -*- coding: utf-8 -*-

import re
import sys
import inspect


class Option(object):
    """
    The Option object for Command.

    :param name: the name of the option, usually like ``-v, --verbose``
    :param description: the description of this option
    :param action: a function to be invoke when this option is found
    :param resolve: a function to transform the option data
    """

    def __init__(self, name, description=None, action=None, resolve=None):
        self.name = name
        self.description = description
        self.action = action
        self.resolve = resolve

    def to_python(self, value):
        """
        Transform the option value to python data.
        """

        if self.resolve:
            return self.resolve(value)
        return value


class Command(object):
    """
    The command interface.

    :param name: program name
    :param description: description of the program
    :param version: version of the program
    :param usage: usage of the program

    Create a :class:`Command` instance in your cli file::

        from terminal import Command
        command = Command('name', 'description', 'version')

    The command will add a default help option. If you set a version
    parameter, it will add a default version option too. You can add
    more options::

        command.option('-v, --verbose', 'show more logs')
        command.option('-o, --output <output>', 'the output file')

    Usually you will need a subcommand feature, add a subcommand like
    this::

        subcommand = Command('build', 'build command')
        subcommand.option('--source <source>', 'source directory')

        command.action(subcommand)

    A subcommand is a full featured Command, which means you can add
    a subcommand to the subcommand too. We can also add a subcommand
    with the decorator feature::

        @command.action
        def build(output='_build'):
            '''
            generate the documentation.

            :param source: the source directory
            '''
            do_something(output)

    After defining the command, we can parse the command line argv::

        command.parse()

    If we have pased ``--verbose`` in the terminal, we can get::

        assert command.verbose is True
    """

    def __init__(self, name, description=None, version=None, usage=None,
                 title=None):
        self._name = name
        self._description = description
        self._version = version
        self._usage = usage
        self._title = title

        self._command_func = None
        self._option_list = []
        self._command_list = []

        self._results = {}
        self._args_results = []

        self.add_default_options()

    def __getitem__(self, key):
        return self._results.get(key)

    def __getattr__(self, key):
        try:
            return super(Command, self).__getattr__(key)
        except AttributeError:
            return self._results.get(key)

    def __call__(self, func):
        return self.action(func)

    @property
    def args(self):
        """
        argv that are not for options.
        """

        return self._args_results

    def get(self, key):
        """
        Get parsed result.

        After :func:`parse` the argv, we can get the parsed results::

            # command.option('-f', 'description of -f')
            command.get('-f')

            command.get('verbose')
            # we can also get ``verbose``: command.verbose
        """

        return self._results.get(key)

    def option(self, name, description=None, action=None, resolve=None):
        """
        Add or get option.

        Here are some examples::

            command.option('-v, --verbose', 'show more log')
            command.option('--tag <tag>', 'tag of the package')
            command.option('-s, --source <source>', 'the source repo')

        :param name: arguments of the option
        :param description: description of the option
        :param action: a function to be invoked
        :param resolve: a function to resolve the data

        """

        if isinstance(name, Option):
            option = name
        else:
            name = name.strip()
            option = Option(
                name=name, description=description,
                action=action, resolve=resolve,
            )

        self._option_list.append(option)
        return self

    def add_default_options(self):
        def print_help():
            self.print_help()
            return sys.exit(0)
        self.option(
            '-h, --help',
            'output the help menu',
            print_help
        )

        if self._version:
            def print_version():
                self.print_version()
                return sys.exit(0)

            self.option(
                '-V, --version',
                'output the version number',
                print_version
            )
        return self

    def add_log_options(self, verbose_func=None, quiet_func=None):
        """
        A helper for setting up log options
        """

        self.option('-v, --verbose', 'show more logs', verbose_func)
        self.option('-q, --quiet', 'show less logs', quiet_func)
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
            name = option.name
            m = regex.findall(name)
            if not m:
                raise RuntimeError('Invalid Option: %s', name)

            shortname, longname, tag = m[0]

            if arg not in (shortname, longname):
                continue

            action = option.action
            if action:
                action()

            if not tag and not longname:
                self._results[shortname] = True
                return True

            if not tag and longname and longname.startswith('--no-'):
                self._results[longname[5:]] = False
                return True

            if not tag and longname:
                self._results[longname[2:]] = True
                return True

            if not tag and not longname:
                self._results[shortname] = True
                return True

            # has tag, it should has value
            if not value:
                if self._argv:
                    value = self._argv[0]
                    self._argv = self._argv[1:]

            if not value:
                raise RuntimeError('Missing value for: %s', name)

            if not longname:
                self._results[shortname] = option.to_python(value)
            else:
                self._results[longname[2:]] = option.to_python(value)
            return True

        return False

    def action(self, command):
        """
        Add a subcommand.

        :param command: a function or a Command

        You can add a :class:`Command` as an action, or a function::

            command.action(subcommand)

        If you prefer a decorator::

            @command.action
            def server(port=5000):
                '''
                docstring as the description

                :param port: description of port
                '''
                start_server(port)

        It will auto generate a subcommand from the ``server`` method.
        """

        if isinstance(command, Command):
            self._command_list.append(command)
            return self

        # it is a function
        func = command
        args, varargs, keywords, defaults = inspect.getargspec(func)
        if not args:
            # a pure function
            self._command_list.append(func)
            return self

        if func.__doc__:
            doclines = func.__doc__.splitlines()
        else:
            doclines = []
        doclines = filter(lambda o: o.strip(), doclines)
        doclines = list(map(lambda o: o.strip(), doclines))

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

        cmd._command_func = func
        self._command_list.append(cmd)
        return self

    def parse(self, argv=None):
        """
        Parse argv of terminal

        :param argv: default is sys.argv
        """

        if not argv:
            argv = sys.argv
        elif isinstance(argv, str):
            argv = argv.split()

        self._argv = argv[1:]
        if not self._argv:
            if self._command_func:
                self._command_func(**self._results)
            return self

        cmd = self._argv[0]

        if not cmd.startswith('-'):
            # parse subcommands
            for command in self._command_list:
                if isinstance(command, Command) and command._name == cmd:
                    command._parent = self
                    return command.parse(self._argv)

                if inspect.isfunction(command) and command.__name__ == cmd:
                    return command()

        while self._argv:
            arg = self._argv[0]
            self._argv = self._argv[1:]
            if not self.parse_options(arg):
                self._args_results.append(arg)

        if hasattr(self, '_parent') and isinstance(self._parent, Command):
            self._parent._args_results = self._args_results

        if self._command_func:
            self._command_func(**self._results)
        return self

    def print_version(self):
        """
        Print the program version.
        """

        if not self._version:
            return self

        if not self._title:
            print('  %s %s' % (self._name, self._version))
            return self

        print('  %s (%s %s)' % (self._title, self._name, self._version))
        return self

    def print_title(self, title):
        """
        Print output the title.

        You can create a colorized title by::

            class MyCommand(Command):

                def print_title(self, title):
                    if 'Options' in title:
                        print(terminal.magenta(title))
                    elif 'Commands' in title:
                        print(terminal.green(title))
                    return self

        You can get the color function with ``terminal``.
        """

        print(title)
        return self

    def print_help(self):
        """
        Print the help menu.
        """

        print('\n  %s %s' % (self._title or self._name, self._version or ''))

        if self._usage:
            print('\n  %s' % self._usage)
        else:
            cmd = self._name
            if hasattr(self, '_parent') and isinstance(self._parent, Command):
                cmd = '%s %s' % (self._parent._name, cmd)

            if self._command_list:
                usage = 'Usage: %s <command> [option]' % cmd
            else:
                usage = 'Usage: %s [option]' % cmd
            print('\n  %s' % usage)

        arglen = max(len(o.name) for o in self._option_list)
        arglen += 2

        self.print_title('\n  Options:\n')
        for o in self._option_list:
            print('    %s %s' % (_pad(o.name, arglen), o.description or ''))
        print('')

        if not self._command_list:
            return self

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
        return self


def _pad(msg, length):
    return '%s%s' % (msg, ' ' * (length - len(msg)))
