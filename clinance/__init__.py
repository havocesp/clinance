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
__all__ = ['__version__', '__license__', '__license__', 'DEBUG', 'BASE_DIR']
