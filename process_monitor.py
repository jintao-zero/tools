import psutil
import logging
import os
import time

"""
use this module to check whether QuoteReceiver service process
is running, otherwise start the service

"""

def init_logger():

    #create logger
    logger_name = "quote_receiver_monitor"
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    #create file handler
    log_path = r"C:\SSEInfoNetMonitor\quote_receiver_monitor.log"
    fh = logging.FileHandler(log_path)
    fh.setLevel(logging.INFO)

    #create stream handler to console
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    #create formatter
    fmt = "%(asctime)s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s"
    datefmt = "%a %d %b %Y %H:%M:%S"
    formatter = logging.Formatter(fmt, datefmt)

    #add handler and formatter to logger
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    ch.setFormatter(formatter)  
    logger.addHandler(ch)

    logger.setLevel(logging.DEBUG)

    return logger

def monitor(process_name):
    logger = init_logger()
    logger.info('monitor process start....')

    while True:
        for proc in psutil.process_iter():
            if proc.name().find(process_name) != -1:
                logger.debug('find %s' % process_name)
                break
            else:
                logger.debug(proc.name())
        else:
            logger.critical('process:%s no found' % process_name)
            cmd = "net start %s " % process_name
            exit_status = os.system(cmd)
            logger.info('%s exit_status %d' % (cmd, exit_status)) 
            time.sleep(2)
        time.sleep(1)

def test(process_name):
    monitor(process_name)
    
if __name__ == '__main__':
    process_name = 'QuoteReceiver'
    test(process_name)
