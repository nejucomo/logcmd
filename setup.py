#!/usr/bin/env python

import os
from setuptools import setup, find_packages

cmdclass={}
if not os.path.isfile('PKG-INFO'):
    # We are not in an sdist, so incorporate qip:
    import qip
    cmdclass.update(qip.get_commands())


setup(name='logcmd',
      description='Run a child command; disambiguate stdout/err; show args, exit status/signal, wall clock time.',
      version='0.2.dev0',
      author='Nathan Wilcox',
      author_email='nejucomo@gmail.com',
      license='GPLv3',
      url='https://github.com/nejucomo/logcmd',
      packages=find_packages(),
      test_suite='logcmd.tests',
      entry_points = {
        'console_scripts': [
            'logcmd = logcmd.main:main',
            ],
        },
     )
