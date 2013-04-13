.. _api:

Developer Interface
===================

This part of the documentation covers the interface of terminal.
Terminal only depends on the built-in battery, it is light weight.

.. module:: terminal


Command Object
--------------

Command is the interface which you can create a command parser.

.. autoclass:: Command
   :members:

Logger Object
-------------

Logger is the interface which you can create a logging instance.
We do have a initialized instance on terminal::

    >>> terminal.log.info('this is the default log instance')

.. autoclass:: Logger
   :members:


Prompt
------

.. autofunction:: prompt
.. autofunction:: prompt_password
.. autofunction:: prompt_bool
.. autofunction:: prompt_choices

Colors
------

.. autoclass:: Color
