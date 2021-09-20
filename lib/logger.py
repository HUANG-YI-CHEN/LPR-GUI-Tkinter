import logging
import os
import time
from time import strftime


class Logger:
    def __init__(self, level, save=False):
        self.debug_level = level
        self.debug_save = save
        self.__logdir = os.path.join(os.path.abspath(os.path.curdir),'log')
        self.__basename = str(strftime("%Y%m%d_%I%M%S", time.localtime())) + '.log'
        self.__filepath = os.path.join(self.__logdir, self.__basename)

    def config(self):
        level = self.debug_level
        format = '%(asctime)s %(levelname)s %(message)s'
        datefmt='%Y-%m-%d %H:%M:%S'
        handlers = None
        if self.debug_save:
            if not os.path.exists(self.__logdir):
                os.mkdir(self.__logdir)
            handlers = [logging.FileHandler(self.__filepath, 'w', 'utf-8')]
        return {'level':level, 'format':format, 'datefmt':datefmt, 'handlers':handlers}
