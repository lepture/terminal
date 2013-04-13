.. _api:

Developer Interface
===================

This part of the documentation covers the interface of terminal.
Terminal only depends on the built-in battery, it is light weight.

.. module:: terminal


Command
-------

Command is the interface which you can create a command parser.

.. autoclass:: Command
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
