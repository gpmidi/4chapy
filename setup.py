#!/usr/bin/python
#===============================================================================
#    This file is part of 4chapy. 
#
#    4chapy is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 2 of the License, or
#    (at your option) any later version.
#
#    4chapy is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with 4chapy.  If not, see http://www.gnu.org/licenses/old-licenses/gpl-2.0.html 
#===============================================================================
''' Install/build 4chapy

@author: paulson mcintyre <paul@gpmidi.net>
'''
from setuptools import setup
import sys
VERSION = "0.4"

# Generate docs
import os
sys.path.append('src')
sys.path.append('examples')

setup(
      name = "python-4chapy",
      version = VERSION,
      description = "Python interface to 4chan's JSON API",
      author = "Paulson McIntyre (GpMidi)",
      author_email = "paul@gpmidi.net",
      license = "GPL",
      long_description = \
"""
A Python interface for accessing and working with 4chan's 
JSON-based API. The API features automatic request rate
throttling, HTTP & HTTPS support, basic caching, and 
an returns easy-to-use objects instead of raw data structures. 
""",
      url = 'https://github.com/gpmidi/4chapy',
      packages = [
                'Fourchapy',
                  ],
      package_dir = {
                   '':'src',
                     },
      scripts = [
                 "examples/DisplayThread.py",
                 "examples/ReadmeExample1.py",
                 "examples/ReadmeExample2.py",
                 ],
      data_files = [],
      classifiers = [
          "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Development Status :: 4 - Beta",
          "Operating System :: OS Independent",
          "Intended Audience :: Developers",
          "Topic :: Communications",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Multimedia :: Graphics",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords = '4chan json http https thread page post',
      install_requires = [
        'distribute',
      ],
      )
