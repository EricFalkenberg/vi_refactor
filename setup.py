#!/usr/bin/env python

from setuptools import setup

setup(name="Vi Refactor",
    version="0.0.3",
    description="CLI tool for refactoring your codebase with vi/m.",
    author="Eric Falkenberg",
    author_email="exf4789@rit.edu",
    url="https://ericfalkenberg.github.io/vi_refactor/",
    scripts=['vi_refactor'],
    data_files=[('.vi_refactor', ['.vi_refactor'])],
)  