Terminal
================================

A terminal environment tools for python.

Color
-------

Color is inspired by fabulus.

::

    >>> from terminal import red
    >>> print red('hello world')


Logging
--------

Colorful and nested logging support::

    from terminal import logging

    logging.start('==> Start Program')
    logging.debug('reading config file')
    logging.debug('loading config file')
    logging.debug('prepare environment')

    # this will be a nested logging
    logging.start('==> Start Reading')
    logging.debug('reading post in content directory')
    logging.info('reading post "Hello World"')
    logging.end('End Reading')

    # another nested logging
    logging.start('==> Start Writing')
    logging.debug('writing post in output directory')
    logging.info('writing post "Hello World"')
    logging.end('End Writing')

    logging.debug('This is a demo for debug')
    logging.info('This is a demo for info')
    logging.warn('This is a demo for warn')
    logging.error('This is a demo for error')
    logging.end('End Program')

.. image: assets/logging.png

Progress bar support::

    import time
    from terminal import logging

    for i in range(20):
        time.sleep(0.1)
        logging.progress(i + 1, 20)


Argument Parser
---------------

TODO
