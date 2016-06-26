#!/usr/bin/env python

from setuptools import setup
from looptimer import __version__


setup(
    name='looptimer',
    version=__version__,
    description='Progress bar style loop timer with projected time-to-completion',
    author='Bryan Johnson',
    author_email='d.bryan.johnson@gmail.com',
    packages=['looptimer'],
    url='https://github.com/dbjohnson/looptimer',
    download_url='https://github.com/dbjohnson/looptimer/tarball/%s' % __version__
)
