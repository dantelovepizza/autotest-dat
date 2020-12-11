import logging
import os
import time
import unittest
from HTMLTestRunner import HTMLTestRunner
from common.op_yaml import conf

# 读取配置文件
title = conf["target"]
description = conf["description"]

# 测试报告/测试用例存储位置配置
now = time.strftime(r'%Y.%m.%d %H-%M-%S')
report_dir = os.path.join(os.getcwd(), r'report', now + '.html')
cases_path = os.path.join(os.getcwd(), r'TestCase')
run_log = os.path.join(os.getcwd(), r'log')

# 测试用例集
discover = unittest.defaultTestLoader.discover(
    cases_path, pattern='test*.py')

if __name__ == '__main__':
    fp = open(report_dir, 'wb')
    runner = HTMLTestRunner(
        stream=fp,
        title=title,
        description=description,
        verbosity=2)
    runner.run(discover)
