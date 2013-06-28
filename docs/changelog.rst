Changelog
=========

Here you can see the full list of changes between each Terminal release.

.. module:: terminal


Version 0.4.0
-------------

Release date to be decided.

* Add alias :meth:`Command.subcommand`
* Add `arguments` parameter for :class:`Command`

Version 0.3.0
-------------

Released on May 7, 2013. Beta release.

* various bugfixed
* delete an newline in print help
* remove support for pure function as action
* config option in docstring
* add help_footer option


Version 0.2.0
-------------

Released on April 23, 2013. Beta release.

* various bugfixed
* don't sys.exit on :meth:`Command.print_help` and :meth:`Command.print_version`
* add :class:`Option`, use :class:`Option` on :meth:`Command.option`
* remove the colorful message on :meth:`Logger.message`
* disable :meth:`Logger.verbose` log on :meth:`Logger.start` and :meth:`Logger.end`
* add **builtin.Command** and **builtin.Logger**
* Option parser has required and boolean flags, Option parser has default value
* record warn and error count on :class:`Logger`


Version 0.1.0
-------------

First public preview release.
