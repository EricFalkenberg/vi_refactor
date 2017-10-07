#!/usr/bin/env python

from setuptools import setup

setup(name="viref",
    version="0.0.5",
    description="CLI tool for refactoring your codebase with vi/m.",
    author="Eric Falkenberg",
    author_email="exf4789@rit.edu",
    url="https://ericfalkenberg.github.io/viref/",
    py_modules=['viref'],
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        viref=viref:cli
    ''',
)  
