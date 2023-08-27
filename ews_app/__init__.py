import os
import logging
import sys

# create logger
logger = logging.getLogger('ews_app')
logger.setLevel(logging.DEBUG)

logger.propagate = 0

# create console handler and set level to debug
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)


# registering services

path = os.path.dirname(os.path.abspath(__file__))

__all__ = []
for py in [f[:-3] for f in os.listdir(path) if f.endswith('.py') and f != '__init__.py' and not f.endswith('interface.py')]:
    __all__.append(py)
