
__author__ = 'zhangjian5'
import time
import logging

level = logging.DEBUG
format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
datefmt = '%yy-%m-%d %H:%M'
"""
    Does Python's time.time() return the local or UTC timestamp?
    http://stackoverflow.com/questions/13890935/does-pythons-time-time-return-the-local-or-utc-timestamp
"""
filename = str(time.time())
filemode = 'w'
logging.basicConfig(level=level, format=format, datefmt=datefmt, filename=filename, filemode=filemode)

# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)
logger = logging.getLogger(__name__)