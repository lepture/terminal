.. _advanced:

Advanced Usage
==============

This document covers some of Terminal more advanced features.

.. module:: terminal


Colorful Life
-------------

If you are not satisfied with 8-bit colors, we can have more.
The :class:`colorize` function can pain 256 colors if your terminal supports 256 colors::

    >>> from terminal import colorize
    >>> print colorize('text', 'red')        # color name
    text
    >>> print colorize('text', '#ff0000')    # hex color with #
    text
    >>> print colorize('text', 'ff0000')     # hex color without #
    text
    >>> print colorize('text', (255, 0, 0))  # rgb color
    text


.. admonition:: Note:

    If your terminal can not show 256 colors, maybe you should change your terminal
    profile, claim that it supports 256 colors.

We can also paint the background of the text with colorize::

    >>> print colorize('text', 'ff0000', background=True)

The source engine of :class:`colorize`, :class:`red`, :class:`cyan` and etc. is
:class:`Color` object. Let's dig into it::

    >>> from terminal import Color
    >>> s = Color('text')
    >>> s.fgcolor = 1
    >>> print s
    text
    >>> s.bgcolor = 2
    >>> print s
    text
    >>> s.styles = [1, 4]
    >>> print s
    text

But it is not fun to play with ANSI code, we like something that we can read::

    >>> s = Color('text')
    >>> s.fgcolor = 'red'
    >>> s.bgcolor = 'green'
    >>> print s

This is not good enough, if we want to paint a text in red text, green background,
bold and underline styles, we could::

    >>> from terminal import *
    >>> print underline(bold(green_bg(red('text'))))
    text
    >>> # this is a disaster, we can do better
    ...
    >>> s = Color('text')
    >>> print s.red.green_bg.bold.underline
    text

.. admonition:: Note:

    If you are colorizing non-ASCII charaters, and you are not on Python 3.
    Please do wrap the charaters with **u**::

        >>> terminal.red(u'中文')


Chain Logging
-------------


Decorator Command
-----------------
