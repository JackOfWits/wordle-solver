import os
import sys
import setuptools

sys.path.insert(0, os.path.dirname(__file__))
import wordle

setuptools.setup(
    name='wordle-solver',
    version=wordle.__version__,
)
