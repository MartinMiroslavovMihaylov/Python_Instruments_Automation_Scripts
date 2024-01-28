# -*- coding: utf-8 -*-
"""
Created on Sat Feb 11 16:00:07 2023

@author: Martin.Mihaylov
"""

from setuptools import setup, find_packages



with open("requirements.txt") as requirement_file:
    requirements = requirement_file.read().split()



setup(
      name='InstrumentControl',                 # This is the name of your PyPI-package.
      description="A SCT Group Labor Instrument Control package.",
      author="Martin.Mihaylov ",
      author_email="<martinmi@mail.uni-paderborn.de>",
      url="<https://martinmiroslavovmihaylov.github.io/Python_Documents/>",
      version='1.2',                          # Update the version number for new releases
      install_requires=requirements  
 )