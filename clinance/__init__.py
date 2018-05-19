#-*- coding:utf-8 -*-
"""
Clinance module
"""
import os
from __main__ import main

__version__ = '0.1.0'
__author__ = 'Daniel J. Umpierrez'
__license__ = 'MIT'

# global debug flag
DEBUG = False
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

if DEBUG:
    print('BASE_DIR: ' + BASE_DIR)

__all__ = ['__version__', '__license__', '__license__', 'DEBUG', 'BASE_DIR', 'main']
