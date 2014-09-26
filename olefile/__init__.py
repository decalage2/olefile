try:
    # first try to import olefile for Python 2.6+/3.x
    from olefile import *
except:
    # if it fails, fallback to the old version olefile2 for Python 2.x:
    from olefile2 import *
