# -*- coding: utf-8 -*-
"""
    terminal.prompt
    ~~~~~~~~~~~~~~~

    Prompt support on terminal.

    :copyright: (c) 2013 by Hsiaoming Yang.
"""

import getpass
import sys

# Python 3
if sys.version_info[0] == 3:
    string_type = str
else:
    string_type = (unicode, str)


def prompt(name, default=None):
    """
    Grab user input from command line.

    :param name: prompt text
    :param default: default value if no input provided.
    """

    prompt = name + (default and ' [%s]' % default or '')
    prompt += name.endswith('?') and ' ' or ': '
    while True:
        try:
            rv = raw_input(prompt)
        except NameError:
            rv = input(prompt)
        if rv:
            return rv
        if default is not None:
            return default


def password(name, default=None):
    """
    Grabs hidden (password) input from command line.

    :param name: prompt text
    :param default: default value if no input provided.
    """

    prompt = name + (default and ' [%s]' % default or '')
    prompt += name.endswith('?') and ' ' or ': '
    while True:
        rv = getpass.getpass(prompt)
        if rv:
            return rv
        if default is not None:
            return default


def confirm(name, default=False, yes_choices=None, no_choices=None):
    """
    Grabs user input from command line and converts to boolean
    value.

    :param name: prompt text
    :param default: default value if no input provided.
    :param yes_choices: default 'y', 'yes', '1', 'on', 'true', 't'
    :param no_choices: default 'n', 'no', '0', 'off', 'false', 'f'
    """

    yes_choices = yes_choices or ('y', 'yes', '1', 'on', 'true', 't')
    no_choices = no_choices or ('n', 'no', '0', 'off', 'false', 'f')

    while True:
        rv = prompt(name + '?', default and yes_choices[0] or no_choices[0])
        if not rv:
            return default
        if rv.lower() in yes_choices:
            return True
        elif rv.lower() in no_choices:
            return False


def choose(name, choices, default=None, resolve=None, no_choice=('none',)):
    """
    Grabs user input from command line from set of provided choices.

    :param name: prompt text
    :param choices: list or tuple of available choices. Choices may be
                    single strings or (key, value) tuples.
    :param default: default value if no input provided.
    :param no_choice: acceptable list of strings for "null choice"
    """

    if not resolve:
        resolve = lambda o: o.lower()

    _choices = []
    options = []

    for choice in choices:
        if isinstance(choice, string_type):
            options.append(choice)
        else:
            options.append("%s [%s]" % (choice[1], choice[0]))
            choice = choice[0]
        _choices.append(choice)

    while True:
        rv = prompt(name + '? - (%s)' % ', '.join(options), default)
        if not rv:
            return default
        rv = resolve(rv)
        if rv in no_choice:
            return None
        if rv in _choices:
            return rv
