# coding: utf-8

import __builtin__
import getpass
from terminal.prompt import prompt, password, confirm, choose


def test_prompt():
    __builtin__.raw_input = lambda name: name
    rv = prompt('what is your name', default='alice')
    assert rv == 'what is your name [alice]: '

    rv = prompt('what is your name')
    assert rv == 'what is your name: '

    __builtin__.raw_input = lambda _: None
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
    __builtin__.raw_input = lambda name: 'y'
    rv = confirm('foo')
    assert rv is True

    __builtin__.raw_input = lambda name: 'n'
    rv = confirm('foo')
    assert rv is False

    __builtin__.raw_input = lambda name: None
    rv = confirm('foo')
    assert rv is False


def test_choose():
    __builtin__.raw_input = lambda name: 'a'
    rv = choose('foo', ['a', 'b'])
    assert rv == 'a'

    __builtin__.raw_input = lambda name: 'none'
    rv = choose('foo', ['a', 'b'])
    assert rv is None
