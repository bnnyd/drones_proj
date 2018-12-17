import logging
def fun1():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.info('1')
    logger.error('1ffff')
    logger.debug('1aaaa')

def fun2():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.info('2')
    logger.error('2ffff')
    logger.debug('2aaaa')

handler = logging.FileHandler('my2.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.info('3')
logger.error('3ffaefawefff')
logger.debug('3aaaa')

fun1()
fun2()
#logging.error('2')
#logging.debug('3')
