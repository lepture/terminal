.. _changelog:

Changelog
=========

Here you can see the full list of changes between each Terminal release.

.. module:: terminal


Version 0.3.0
-------------

Release date to be decided.

* various bugfixed
* delete an newline in print help
* remove support for pure function as action
* config option in docstring
* add help_footer option


Version 0.2.0
-------------

Released on April 23, 2013. Beta release.

* various bugfixed
* don't sys.exit on :class:`Command.print_help` and :class:`Command.print_version`
* add :class:`Option`, use :class:`Option` on :class:`Command.option`
* remove the colorful message on :class:`Logger.message`
* disable :class:`Logger.verbose` log on :class:`Logger.start` and :class:`Logger.end`
* add **builtin.Command** and **builtin.Logger**
* Option parser has required and boolean flags, Option parser has default value
* record warn and error count on :class:`Logger`


Version 0.1.0
-------------

First public preview release.
