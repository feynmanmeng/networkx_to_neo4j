import logging
import os
import time

class MyLogger():
    '''
    https://bbs.huaweicloud.com/blogs/387797
    https://blog.csdn.net/dadaowuque/article/details/104527196
    读取日志文件，日志格式符合 idealog 默认标准
    日志文件不存在自动创建

    level='INFO',
    path=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs'),  # 在my_logger本目录下的log目录
    fname='test_log'):  # self.__class__.__name__
    '''

    def __init__(self, level, path, fname):
        # 日志器对象
        self.level = level
        self.fname = fname
        self.logger = logging.getLogger(self.fname)
        self.logger.setLevel(level)

        current_time = str(time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()))  # 获取当前时间
        self.path_y_m_d = os.path.join(path, current_time[:10])
        # 检查日志文件夹是否创建，没有则创建
        if not os.path.exists(self.path_y_m_d):
            os.makedirs(self.path_y_m_d, exist_ok=True)
        # 日志保存路径
        self.faddr = os.path.join(self.path_y_m_d, self.fname + "_" + current_time + ".log")
        print(f'日志保存路径：{self.faddr}')

    def console_handle(self):
        '''控制台处理器'''
        console_handle = logging.StreamHandler()
        console_handle.setLevel(self.level)
        console_handle.setFormatter(self.get_formatter()[0])
        return console_handle

    def file_handle(self):
        '''文件处理器'''
        # 检查文件是否存在
        if not os.path.exists(self.faddr):
            # 如果文件不存在，则创建空文件
            with open(self.faddr, 'w'):
                pass
                print(f"未发现[{self.fname}]日志文件，已新建。")
        else:
            print(f"发现[{self.fname}]日志文件。")

        file_handler = logging.FileHandler(self.faddr, mode="a", encoding="utf-8")

        file_handler.setLevel(self.level)
        file_handler.setFormatter(self.get_formatter()[1])
        return file_handler

    # def file_handle_v2(self):
    #     '''文件处理器'''
    #     # TimedRotatingFileHandler支持按时间间隔自动产生文件
    #     # when为时间间隔选项，这里设置为'd'(day)，interval为间隔数，这里设置为1
    #     # 意味着每天产生新的日志文件
    #     file_handler = TimedRotatingFileHandler(self.path, when='d', interval=1, backupCount=7, encoding="utf-8")
    #
    #     file_handler.setLevel(self.level)
    #     file_handler.setFormatter(self.get_formatter()[1])
    #     return file_handler

    def get_formatter(self):
        '''格式器，定义输出格式'''
        # console_fmt = logging.Formatter(fmt = "%(asctime)s %(levelname)s %(filename)s [line:%(lineno)d] %(message)s")
        # file_fmt = logging.Formatter(fmt = "%(asctime)s %(levelname)s [line:%(lineno)d] %(message)s")

        # console_fmt = logging.Formatter(
        #     fmt="%(asctime)s %(levelname)s %(filename)s [line:%(lineno)d] [func:%(funcName)s] %(message)s")
        # file_fmt = logging.Formatter(
        #     fmt="%(asctime)s %(levelname)s %(filename)s [line:%(lineno)d] [func:%(funcName)s] %(message)s")

        console_fmt = logging.Formatter(fmt="%(asctime)s %(levelname)s %(filename)s [line:%(lineno)d] %(message)s")
        file_fmt = logging.Formatter(fmt="%(asctime)s %(levelname)s %(filename)s [line:%(lineno)d] %(message)s")
        return console_fmt, file_fmt

    def get_logger(self):
        if not self.logger.handlers:
            # 日志器添加控制台处理器
            self.logger.addHandler(self.console_handle())
            # 日志器添加文件处理器
            self.logger.addHandler(self.file_handle())
        # 返回日志实例对象
        return self.logger

