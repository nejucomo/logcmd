#!/usr/bin/env python

from distutils.core import setup

setup(name='logcmd',
      description='Run a child command; disambiguate stdout/err; show args, exit status/signal, wall clock time.',
      version='0.1',
      author='Nathan Wilcox',
      author_email='nejucomo@gmail.com',
      license='GPLv3',
      #url='FIXME',
      py_modules=['logcmd'],
      scripts=['logcmd'],
     )
