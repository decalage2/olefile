#!/usr/bin/env python
# import setup
# import sys
#
# argv0 = sys.argv[0]
#
# # create a source distrib in zip and tar.gz formats + upload to PyPI
# sys.argv = [argv0, 'sdist', '--formats=gztar,zip', 'upload']
# setup.main()
#
# raw_input('Press [Enter]')

import subprocess

subprocess.check_call(['python', 'setup.py', 'sdist', '--formats=gztar,zip', 'upload'])

