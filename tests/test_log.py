from terminal import Logger


class TestLogger(object):
    def test_config(self):
        log = Logger()

        log.config(indent=2)
        assert log._indent is 2

        log.config(verbose=True, quiet=True)
        assert log._enable_verbose is True
        assert log._enable_quiet is True

    def test_message(self):
        log = Logger()
        assert log.message('unknown', 'foo', 'bar') == 'foo bar'

    def test_verbose(self):
        log = Logger()
        assert log._is_verbose is False
        assert log.verbose._is_verbose is True

    def test_log(self):
        log = Logger()
        log.debug('debug message')
        log.info('info message')
        log.warn('warn message')
        log.error('error message')

        log.verbose.info('verbose info message')
        log.config(verbose=True)
        log.verbose.info('verbose info message')

        log.start('start message')
        log.info('info message')
        log.end('end message')

        log.config(quiet=True)
        log.debug('debug message')
        log.info('info message')

        log.start('start message')
        log.end()
