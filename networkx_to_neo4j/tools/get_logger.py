import os.path

from .my_logger import MyLogger

level = 'INFO'
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../logs')
fname = 'neo4j_plot'  # self.__class__.__name__

log = MyLogger(level=level, path=path, fname=fname)
logger = log.get_logger()
