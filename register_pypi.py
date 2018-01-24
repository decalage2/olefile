#!/usr/bin/env python
# import setup
# import sys
#
# argv0 = sys.argv[0]
#
# # register version to PyPI
# sys.argv = [argv0, 'register']
# setup.main()
#
# raw_input('Press [Enter]')

import subprocess

subprocess.check_call(['python', 'setup.py', 'register'])

