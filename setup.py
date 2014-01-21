#!/usr/bin/env python

from setuptools import setup

def read_readme(fname):
    try:
       import pypandoc
       return pypandoc.convert('README.md', 'rst')
    except (IOError, ImportError):
       return ''


setup(
    name = 'jsoncompare',
    version = '0.1.0',
    description = 'Json comparison tool',
    author = 'Daniel Myers',
    author_email = 'dmandroid88@gmail.com',
    url = 'https://github.com/dandroid88/jsoncompare',
    packages = ['jsoncompare', 'jsoncompare.tests'],
    keywords = 'json comparison compare order',
    long_description = read_readme('README.md')
)