# Name: Sipeng He
# UCID: 30113342
# Feature: setup file to complie the Cython code.
# Date: 2021.11.23
from distutils.core import setup
from Cython.Build import cythonize

setup(name='GPIO', ext_modules = cythonize("gpio.pyx"))