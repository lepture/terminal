# -*- coding: utf-8 -*-

import re
import sys
import inspect
from collections import OrderedDict


class Command(object):
    """
    The command interface.

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

    @property
    def args(self):
        return self._rests

    def get(self, key):
        return self._results.get(key)

    def option(self, name, description, action=None):
        """
        Add or get option.

        :param name: arguments of the option
        :param description: description of the option

        ::
            command.option('-v, --verbose', 'show more log')
            command.option('--tag <tag>', 'tag of the package')
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
                if isinstance(command, Command) and command.name == cmd:
                    command._parent = self
                    return command.parse(self._args)

                if inspect.isfunction(command) and command.__name__ == cmd:
                    return command()

        while self._args:
            arg = self._args[0]
            self._args = self._args[1:]
            if not self.parse_options(arg):
                self._rests.append(arg)

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
