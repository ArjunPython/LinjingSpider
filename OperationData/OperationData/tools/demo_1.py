# -*- coding: utf-8 -*-
# author: Arjun
# @Time: 18-7-5 下午2:18




import logging


LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='./my.log', level=logging.DEBUG, format=LOG_FORMAT)
# logging.debug("This is a debug log.")
logging.info("This is a info log.")
logging.warning("This is a warning log.")
logging.error("This is a error log.")
logging.critical("This is a critical log.")

def sing():
    sing = logging.debug("This is log.")
    print(sing)

if __name__ == '__main__':
    sing()




