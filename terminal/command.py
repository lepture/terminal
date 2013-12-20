# -*- coding: utf-8 -*-
"""
    terminal.command
    ~~~~~~~~~~~~~~~~

    Command and option parser for terminal.

    :copyright: (c) 2013 by Hsiaoming Yang.
"""

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

        self.parse(name, description)

    def __str__(self):
        return self.key

    def __repr__(self):
        return '<Option "%s">' % str(self)

    def parse(self, name, description):
        """
        Parse option name.

        :param name: option's name
        :param description: option's description

        Parsing acceptable names:

            * -f: shortname
            * --force: longname
            * -f, --force: shortname and longname
            * -o <output>: shortname and a required value
            * -o, --output [output]: shortname, longname and optional value

        Parsing default value from description:

            * source directory, default: src
            * source directory, default: [src]
            * source directory, default: <src>
        """

        name = name.strip()

        if '<' in name:
            self.required = True
            self.boolean = False
            name = name[:name.index('<')].strip()
        elif '[' in name:
            self.required = False
            self.boolean = False
            name = name[:name.index('[')].strip()
        else:
            self.required = False
            self.boolean = True

        regex = re.compile(r'(-\w)?(?:\,\s*)?(--[\w\-]+)?')

        m = regex.findall(name)
        if not m:
            raise ValueError('Invalid Option: %s', name)

        shortname, longname = m[0]

        if not shortname and not longname:
            raise ValueError('Invalid Option: %s', name)

        self.shortname = shortname
        self.longname = longname

        # parse store key
        if longname and longname.startswith('--no-'):
            self.key = longname[5:]
        elif longname:
            self.key = longname[2:]
        else:
            self.key = shortname

        if self.boolean:
            # boolean don't need to parse from description
            if longname and longname.startswith('--no-'):
                self.default = True
            else:
                self.default = False
            return self

        if not description:
            self.default = None
            return self

        # parse default value from description
        regex = re.compile(r'\sdefault:(.*)$')
        m = regex.findall(description)
        if not m:
            self.default = None
            return self

        # if it has a default value, it is not required
        self.required = False

        value = m[0].strip()
        if value.startswith('<') and value.endswith('>'):
            value = value[1:-1]
        elif value.startswith('[') and value.endswith(']'):
            value = value[1:-1]

        self.default = value.strip()
        return self

    def to_python(self, value=None):
        """
        Transform the option value to python data.
        """

        if value is None:
            return self.default

        if self.resolve:
            return self.resolve(value)
        return value


class Command(object):
    """
    The command interface.

    .. versionadded:: 0.4
        The `arguments` parameters were added.

    :param name: name of the program
    :param description: description of the program
    :param version: version of the program
    :param usage: usage of the program
    :param title: title of the program
    :param func: command function to be invoked
    :param arguments: positional arguments

    Create a :class:`Command` instance in your cli file::

        from terminal import Command
        command = Command('name', 'description', 'version')

    The command will add a default help option. If you set a version
    parameter, it will add a default version option too. You can add
    more options::

        command.option('-v, --verbose', 'show more logs')

        # required option in < and >
        command.option('-o, --output <output>', 'the output file')

        # optional option in [ and ]
        command.option('-o, --output [output]', 'the output file')

        # set a default value in description
        command.option('-o, --source [dir]', 'the output file, default: src')

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

            :param output: the output directory
            '''
            do_something(output)

    After defining the command, we can parse the command line argv::

        command.parse()

    If we have pased ``--verbose`` in the terminal, we can get::

        assert command.verbose is True
    """

    def __init__(self, name, description=None, version=None, usage=None,
                 title=None, func=None, help_footer=None, arguments=None):
        self._name = name
        self._description = description
        self._version = version
        self._usage = usage
        self._title = title
        self._command_func = func
        self._help_footer = help_footer
        self._positional_list = arguments or []

        self._parent = None
        self._option_list = []
        self._command_list = []

        self._results = {}
        self._args_results = []

        self._add_default_options()

    def __getitem__(self, key):
        return self.get(key)

    def __getattr__(self, key):
        try:
            return object.__getattribute__(self, key)
        except AttributeError:
            try:
                return self.get(key)
            except ValueError:
                raise AttributeError('No such attribute: %s' % key)

    def __call__(self, func):
        return self.action(func)

    @property
    def args(self):
        """
        argv that are not for options.
        """

        return self._args_results

    def keys(self):
        return self._results.keys()

    def get(self, key):
        """
        Get parsed result.

        After :func:`parse` the argv, we can get the parsed results::

            # command.option('-f', 'description of -f')
            command.get('-f')

            command.get('verbose')
            # we can also get ``verbose``: command.verbose
        """

        value = self._results.get(key)
        if value is not None:
            return value

        # get from option default value
        option = list(filter(lambda o: o.key == key, self._option_list))
        if not option:
            raise ValueError('No such option: %s' % key)

        option = option[0]
        return option.default

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

    def _add_default_options(self):
        def print_help():  # pragma: no cover
            self.print_help()
            return sys.exit(0)

        self.option(
            '-h, --help',
            'output the help menu',
            print_help
        )

        if self._version:
            def print_version():  # pragma: no cover
                self.print_version()
                return sys.exit(0)

            self.option(
                '-V, --version',
                'output the version number',
                print_version
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

        for option in self._option_list:

            if arg not in (option.shortname, option.longname):
                continue

            action = option.action
            if action:
                action()

            if option.key == option.shortname:
                self._results[option.key] = True
                return True

            if option.boolean and option.default:
                self._results[option.key] = False
                return True

            if option.boolean:
                self._results[option.key] = True
                return True

            # has tag, it should has value
            if not value:
                if self._argv:
                    value = self._argv[0]
                    self._argv = self._argv[1:]

            if not value:
                raise RuntimeError('Missing value for: %s' % option.name)

            self._results[option.key] = option.to_python(value)
            return True

        return False

    def validate_options(self):
        """
        Validate options
        """
        for option in self._option_list:
            # validate options
            if option.required and option.key not in self._results:
                raise RuntimeError('Option %s is required.' % option.name)

    def action(self, command):
        """
        Add a subcommand. (Alias `subcommand`).

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
            return command

        # it is a function
        func = command
        args, varargs, keywords, defaults = inspect.getargspec(func)

        if func.__doc__:
            doclines = func.__doc__.splitlines()
        else:
            doclines = []
        doclines = filter(lambda o: o.strip(), doclines)
        doclines = list(map(lambda o: o.strip(), doclines))

        params = {}
        options = {}
        usage = None

        for line in doclines:
            if line.startswith('usage:'):
                usage = line[6:].strip()
            elif line.startswith(':param '):
                name, desc = line[7:].split(':', 1)
                params[name.strip()] = desc.strip()
            elif line.startswith(':option '):
                name, desc = line[8:].split(':', 1)
                options[name.strip()] = desc.strip()

        desc = None
        if doclines:
            desc = doclines[0]

        # use self.__class__ instead of Command for inherit
        cmd = self.__class__(func.__name__, desc, usage=usage)

        defaults = defaults or []
        kwargs = dict(zip(*[reversed(i) for i in (args, defaults)]))

        for arg in args:
            desc = params.get(arg, None)
            name = options.get(arg, None)
            if arg in kwargs:
                value = kwargs[arg]
                if value is True:
                    name = name or '--no-%s' % arg
                    option = Option(name, desc)
                elif value is False:
                    name = name or '-%s, --%s' % (arg[0], arg)
                    option = Option(name, desc)
                else:
                    name = name or '-%s, --%s [%s]' % (arg[0], arg, arg)
                    option = Option(name, desc)
                    option.default = value

                cmd.option(option)
            elif desc:
                # if has description, it is a required option
                name = name or '-%s, --%s <%s>' % (arg[0], arg, arg)
                cmd.option(name, desc)
            else:
                # positional arguments
                cmd._positional_list.append(arg)

        cmd._command_func = func
        self._command_list.append(cmd)
        return command

    def subcommand(self, command):
        """Alias for Command.action."""
        return self.action(command)

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
            self.validate_options()
            if self._command_func:
                self._command_func(**self._results)
                return True
            return False

        cmd = self._argv[0]

        if not cmd.startswith('-'):
            # parse subcommands
            for command in self._command_list:
                if isinstance(command, Command) and command._name == cmd:
                    command._parent = self
                    return command.parse(self._argv)

        _positional_index = 0
        while self._argv:
            arg = self._argv[0]
            self._argv = self._argv[1:]
            if not self.parse_options(arg):
                self._args_results.append(arg)
                if len(self._positional_list) > _positional_index:
                    # positional arguments
                    key = self._positional_list[_positional_index]
                    self._results[key] = arg
                    _positional_index += 1

        # validate
        self.validate_options()

        if self._parent and isinstance(self._parent, Command):
            self._parent._args_results = self._args_results

        if self._command_func:
            self._command_func(**self._results)
            return True
        return False

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

            pos = ' '.join(['<%s>' % name for name in self._positional_list])
            print('\n  %s %s' % (usage, pos))

        arglen = max(len(o.name) for o in self._option_list)
        arglen += 2

        self.print_title('\n  Options:\n')
        for o in self._option_list:
            print('    %s %s' % (_pad(o.name, arglen), o.description or ''))
        print('')

        if self._command_list:
            self.print_title('  Commands:\n')
            for cmd in self._command_list:
                if isinstance(cmd, Command):
                    name = _pad(cmd._name, arglen)
                    desc = cmd._description or ''
                    print('    %s %s' % (_pad(name, arglen), desc))

            print('')

        if self._help_footer:
            print(self._help_footer)
            print('')

        return self


def _pad(msg, length):
    return '%s%s' % (msg, ' ' * (length - len(msg)))
