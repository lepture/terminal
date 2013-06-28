Developer Interface
===================

This part of the documentation covers the interface of terminal.
Terminal only depends on Python's built-in batteries, it is lightweight.

.. module:: terminal


Command
-------

Command is the interface which you can create a command parser.

.. autoclass:: Command
   :members:


.. autoclass:: Option
   :members:


Logger
------

Logger is the interface which you can create a logging instance.
We do have a initialized instance on terminal::

    >>> terminal.log.info('this is the default log instance')

.. autoclass:: Logger
   :members:


Prompt
------

Prompt are functions to communicate with the terminal.

.. autofunction:: prompt
.. autofunction:: password
.. autofunction:: confirm
.. autofunction:: choose

Colors
------

.. autoclass:: Color

.. autofunction:: colorize


Front colors
~~~~~~~~~~~~

.. autofunction:: black
.. autofunction:: red
.. autofunction:: green
.. autofunction:: yellow
.. autofunction:: blue
.. autofunction:: magenta
.. autofunction:: cyan
.. autofunction:: white

Background colors
~~~~~~~~~~~~~~~~~

.. autofunction:: black_bg
.. autofunction:: red_bg
.. autofunction:: green_bg
.. autofunction:: yellow_bg
.. autofunction:: blue_bg
.. autofunction:: magenta_bg
.. autofunction:: cyan_bg
.. autofunction:: white_bg

Styles
~~~~~~

.. autofunction:: bold
.. autofunction:: faint
.. autofunction:: italic
.. autofunction:: underline
.. autofunction:: blink
.. autofunction:: overline
.. autofunction:: inverse
.. autofunction:: conceal
.. autofunction:: strike
