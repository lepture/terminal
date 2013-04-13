# coding: utf-8

from terminal import log

log.info('hello test')

log.start('start a level')
log.info('hell in a level')
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
