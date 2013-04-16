from terminal.builtin import log

log.start('terminal build')
log.info('build foo')
log.debug('read file foo.py')
log.warn('not found foo.py')
log.info('build bar')
log.debug('read file bar.py')
log.start('sub read')
log.info('parse bar.py')
log.info('bar is python')
log.end('parse end')
log.error('syntax error')
log.end('end build')
