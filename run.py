import time
from terminal import logging

logging.start('Start Application')
logging.debug('hello debug')
logging.info('hello info')
logging.warn('hello warn')
logging.error('hello error')

logging.start('Second start')
logging.info('hello info')
logging.end()

logging.end()

for i in range(10):
    logging.progress(i + 1, 10)
    time.sleep(0.5)
