Terminal
================================

A better terminal tools for python.


Color
-------

Color is inspired by fabulus.

::

    >>> import terminal
    >>> print terminal.red('hello world')


Log
--------

Nested and verbose supported logging.

::

    >> import terminal
    >> terminal.log.info('hello')
    >> terminal.log.verbose.info('hello')
    >> terminal.log.config(verbose=True)
    >> terminal.log.verbose.info('hello')


Command
--------

A simple and better argparser for python::

    from terminal import Command
    from terminal import log

    program = Command(name='terminal', version='1.0.0')

    program.option('-v, --verbose', 'show more logs')
    program.parse()

    if program.verbose:
        log.config(verbose=True)
