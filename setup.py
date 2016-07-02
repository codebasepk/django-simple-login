# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-

#
# Simple Login
# Copyright (C) 2016 byteShaft
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import os
from setuptools import (
    find_packages,
    setup,
)


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-simple-login',
    version='0.2',
    packages=find_packages(),
    include_package_data=True,
    license='GNU GPL Version 3',
    description='A simple django app to make accounts creation a breeze.',
    long_description=README,
    url='https://github.com/byteshaft/django-simplelogin',
    download_url='https://github.com/byteShaft/django-simplelogin/tarball/0.2',
    author='Omer Akram',
    author_email='om26er@gmail.com',
    keywords=['django', 'accounts'],
    classifiers=[],
)
