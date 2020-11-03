#!/usr/bin/env python

# create a source distribution in zip format, and a universal wheel distribution (python 2+3)
# pip will install the universal wheel by default
# upload: twine upload dist/*.whl dist/*.zip

# references:
# https://stackoverflow.com/questions/30438216/how-do-i-upload-a-universal-python-wheel-for-python-2-and-3
# https://packaging.python.org/guides/distributing-packages-using-setuptools/#universal-wheels

import subprocess

subprocess.check_call(['python', 'setup.py', 'sdist', '--formats=zip', 'bdist_wheel', '--universal'])
