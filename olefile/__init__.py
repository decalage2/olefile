try:
    # first try to import olefile for Python 2.6+/3.x
    from .olefile import *
    # import metadata not covered by *:
    from .olefile import __doc__, __version__, __author__, __date__

except:
    # if it fails, fallback to the old version olefile2 for Python 2.x:
    from .olefile2 import *
    # import metadata not covered by *:
    from .olefile2 import __doc__, __version__, __author__, __date__
