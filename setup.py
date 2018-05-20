# -*- coding:utf-8 -*-
from setuptools import setup, find_packages

from clinance import __version__, __author__, __package__, __email__, __license__, __description__, __keywords__

setup(
    name=__package__,
    version=__version__,
    packages=find_packages(exclude=['.idea*', 'build*', 'clinance.egg-info*', 'dist*', 'venv*', 'doc*', 'test*']),
    url='https://github.com/havocesp/{}'.format(__package__),
    license=__license__,
    entry_points={
        'console_scripts': ['clinance=clinance.cli:main'],
    },
    # scripts={'':''},
    packages_dir={'': __package__},
    keywords=__keywords__,
    author=__author__,
    author_email=__email__,
    dependency_links=[
        'http://github.com/havocesp/finta',
        'http://github.com/havocesp/panance'],
    long_description=__description__,
    description='Binance client from CLI.',
    classifiers=[
        'Development Status :: 4 - Beta',
        #        'Intended Audience :: Developers',
        #        'Topic :: Software Development :: Open source Binance interface from CLI',
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
