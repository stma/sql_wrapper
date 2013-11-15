#!/usr/bin/python

from setuptools import setup
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="sql_wrapper",
    version="0.1",
    description="Python module for retrieve data from \
relational databases by queries writen in python-sql.",
    author="Matyas Steiner",
    author_email="steiner.matyas@gmail.com",
    url="https://github.com/stma/sql_wrapper",
    license="GNU GPL v2",
    long_description=read('README.md'),
    py_modules=["sql_wrapper"],
    install_requires=[
        "python-sql==0.2",
        "psycopg2==2.5.1",
    ],
)
