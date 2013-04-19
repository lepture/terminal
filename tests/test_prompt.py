# coding: utf-8

import getpass
from terminal.prompt import prompt, password, confirm, choose


def patch(fn):  # pragma: no cover
    try:
        import __builtin__
        __builtin__.raw_input = fn
    except ImportError:
        import builtins
        builtins.input = fn


def test_prompt():
    patch(lambda name: name)
    rv = prompt('what is your name', default='alice')
    assert rv == 'what is your name [alice]: '

    rv = prompt('what is your name')
    assert rv == 'what is your name: '

    patch(lambda _: None)
    rv = prompt('what is your name', default='alice')
    assert rv == 'alice'


def test_password():
    getpass.getpass = lambda name: 'a'
    rv = password('foo')
    assert rv == 'a'

    getpass.getpass = lambda name: None
    rv = password('foo', 'a')
    assert rv == 'a'


def test_confirm():
    patch(lambda name: 'y')
    rv = confirm('foo')
    assert rv is True

    patch(lambda name: 'n')
    rv = confirm('foo')
    assert rv is False

    patch(lambda name: None)
    rv = confirm('foo')
    assert rv is False


def test_choose():
    patch(lambda name: 'a')
    rv = choose('foo', ['a', 'b'])
    assert rv == 'a'

    patch(lambda name: 'none')
    rv = choose('foo', ['a', 'b'])
    assert rv is None
