from terminal.builtin import Command, log


def test_command():
    program = Command('foo')

    @program.action
    def lepture(bar):
        assert bar == 'lepture'

    program.print_help()
    program.parse('foo lepture --bar lepture')
    program.print_title('hello')


def test_log():
    log.info('hello test')

    log.start('start a level')
    log.info('info in a level')
    log.warn('warn in a level')
    log.error('error in a level')
    log.debug('debug info')
    log.verbose.info('will not print this')
    log.config(verbose=True)
    log.verbose.info('will print this')

    log.start('start second level')
    log.verbose.debug('hello debug')
    log.end()
    log.config(quiet=True)
    log.info('will not print')
    log.end('close a level')
    log.message('foo', 'bar')
