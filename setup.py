import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-simple-login',
    version='0.6.2',
    packages=['simple_login', 'simple_login.apps',
              'simple_login.utils', 'simple_login.views',
              'simple_login.models', 'simple_login.managers',
              'simple_login.exceptions', 'simple_login.serializers'],
    url='https://github.com/byteshaft/django-simple-login',
    license='GNU GPL Version 3',
    author='Omer Akram',
    author_email='om26er@gmail.com',
    description='A simple django app to make accounts creation a breeze.',
    long_description=README,
    download_url='https://github.com/byteShaft/django-simple-login/tarball/'
                 '0.6.2',
    keywords=['django', 'accounts'],
    classifiers=[],
    install_requires=['django', 'djangorestframework'],
)
