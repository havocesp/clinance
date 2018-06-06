# -*- coding:utf-8 -*-
"""
Clinance module
"""
import os
import sys

__package__ = 'clinance'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# global debug flag
DEBUG = False
globals().update(DEBUG=DEBUG)
globals().update(BASE_DIRG=BASE_DIR)
if DEBUG:
    print('BASE_DIR: ' + BASE_DIR)

__version__ = '0.1.1'
__author__ = 'Daniel J. Umpierrez'
__license__ = 'MIT'
__email__ = 'umpierrez@pm.me'
__description__ = 'A command line interface (CLI) client for Binance cryptocurrency exchange.'
__keywords__ = 'binance cli terminal console client trading altcoin exchange finance market bitcoin cryptocurrency ' \
               'cryptocurrencies crypto-currencies crypto-currency'
__dependencies__ = list({
    'pantulipy',
    'tabulate',
    'begins'
})
__all__ = ['__version__', '__email__', '__package__', '__author__', '__description__', '__license__', '__keywords__',
           '__dependencies__', 'DEBUG', 'BASE_DIR']
