# -*- coding:utf-8 -*-
"""
Clinance module
"""
import os
import sys

__package__ = 'clinance'

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

# global debug flag
DEBUG = False

if DEBUG:
    print('BASE_DIR: ' + BASE_DIR)

__version__ = '0.1.0'
__author__ = 'Daniel J. Umpierrez'
__license__ = 'MIT'
__email__ = 'umpierrez@pm.me'
__description__ = 'A command line interface (CLI) client for Binance cryptocurrency exchange.'
__keywords__ = 'binance cli terminal console client trading altcoin exchange finance market bitcoin cryptocurrency ' \
               'cryptocurrencies crypto-currencies crypto-currency'
__all__ = ['__version__', '__email__', '__package__', '__author__', '__description__', '__license__', '__keywords__',
           'DEBUG', 'BASE_DIR']
