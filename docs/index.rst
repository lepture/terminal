.. terminal documentation master file, created by
   sphinx-quickstart on Fri Apr 12 23:10:45 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Terminal: for Simple and Beautiful
==================================

Terminal is designed for creating terminal-based tools, written in Python,
for developers who like simple and beautiful things.

Python's standard **logging** and **argparse** (or optparse) modules are
powerful, but the API is thoroughly ugly and hard to use. Terminal is
designed to make life simpler and better.

It contains everything you need for terminal:

* Argv Parser
* ANSI Colors
* Prompts
* Logging

::

    from terminal import Command, red

    program = Command('foo', version='1.0.0')

    @program.action
    def show(color=True):
        """
        show something.

        :param color: disable or enable colors
        """
        if color:
            print(red('show'))
        else:
            print('show')


User's Guide
------------

This part of the documentation, which is mostly prose, begins with some
background information about Terminal, then focuses on step-by-step
instructions for getting the most out of Terminal.

.. toctree::
   :maxdepth: 2

   intro
   install
   quickstart
   advanced

API Documentation
-----------------

If you are looking for information on a specific function, class or method,
this part of the documentation is for you.

.. toctree::
   :maxdepth: 2

   api

Additional Notes
----------------

Contribution guide, legal information and changelog are here.

.. toctree::
   :maxdepth: 2

   contrib
   changelog
   authors
