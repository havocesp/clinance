# -*- coding:utf-8 -*-
from setuptools import setup, find_packages

from clinance import __version__, __author__

setup(
    name='clinance',
    version=__version__,
    packages=find_packages(exclude=['.idea*', 'venv*', 'doc*', 'test*']),
    url='https://github.com/havocesp/clinance',
    license='MIT',
    entry_points={
        'console_scripts': ['clinance=clinance.cli:main'],
    },
    packages_dir={'': 'clinance'},
    keywords='binance cli terminal console client trading altcoin exchange finance market bitcoin cryptocurrency cryptocurrencies crypto-currencies crypto-currency',
    author=__author__,
    author_email='',
    dependency_links=['http://github.com/havocesp/finta', 'http://github.com/havocesp/panance'],
    long_description='A command line interface (CLI) client for Binance cryptocurrency exchange.',
    description='Binance client from CLI.',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Binance users',
        'Topic :: Software Development :: Open source Binance interface from CLI',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=[
        'panance',
        'finta',
        'tabulate',
        'defopt'
    ]
)
