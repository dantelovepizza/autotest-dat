import logging
import os
import time

_Level = {
    'CRITICAL': logging.CRITICAL,
    'ERROR': logging.ERROR,
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG,
}


class log_handler(logging.Logger):
    def __init__(self,
                 name,
                 level="INFO",
                 file=None,
                 log_format=None,
                 stream=None):
        super().__init__(name)
        # 设置日志等级
        self.setLevel(level)
        # 设置日志格式
        fmt = logging.Formatter(log_format)
        # 设置日志等级过滤器
        filters = logging.Filter()
        filters.filter = lambda record: record.levelno == logging_level(self.level)
        # 日志保存到指定路径文件下
        if file:
            # 日志存储位置
            file_handler = logging.FileHandler(file, encoding="utf-8", mode="a")
            # 添加过滤器
            file_handler.addFilter(filters)
            # 设置日志输出等级
            file_handler.setLevel(level)
            # 设置日志输出格式
            file_handler.setFormatter(fmt)
            self.addHandler(file_handler)
        if stream:
            # 日志输出到控制台
            ch = logging.StreamHandler()
            ch.addFilter(filters)
            ch.setLevel(level)
            ch.setFormatter(fmt)
            self.addHandler(ch)


# 返回日志输出等级:logging.ERROR
def logging_level(level):
    if isinstance(level, int):
        rv = level
    elif str(level) == level:
        if level not in _Level:
            raise ValueError("Unknown level: %r" % level)
        rv = _Level[level]
    else:
        raise TypeError("Level not a valid string: %r" % level)
    return rv


# 日志格式
fmts = '"%(asctime)s - %(levelname)s: %(message)s"'
# 日志位置
now = time.strftime("%Y.%m.%d")
paths = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
info_path = os.path.join(paths, 'log', now + '_info.log')
error_path = os.path.join(paths, 'log', now + '_error.log')


# 创建通用日志logger，供其他模块调用
info_log = log_handler("info_log", level="INFO", file=info_path, log_format=fmts)
error_log = log_handler("error_log", level="ERROR", stream=True, file=error_path, log_format=fmts)

