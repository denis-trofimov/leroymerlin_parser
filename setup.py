#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(name="leroy_merlin_parser", packages=find_packages(), 
    install_requires=["requests", "bs4", "flask", "flask_sqlalchemy"])
