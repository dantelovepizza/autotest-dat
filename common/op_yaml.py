import os
import yaml
from common.op_log import error_log


class yaml_handler:
    """
    读取.yaml配置文件
    """

    # 通过当前文件所在路径定位配置文件位置
    def __init__(self, file):
        self.file = file

    def read_yaml(self, encoding="utf-8"):
        """读取yaml文件数据"""
        if os.path.isfile(self.file):
            try:
                yaml_file = open(file=self.file, mode='r', encoding=encoding)
                conf = yaml_file.read()
                return yaml.load(conf, Loader=yaml.FullLoader)
            except FileNotFoundError as File:
                error_log.error(File)
            except IOError as IO:
                error_log.error(IO)
            except Exception as e:
                error_log.error(e)
        else:
            error_log.error("读取路径文件不存在！")

    def write_yaml(self, data, encoding='utf-8'):
        """向yaml文件写入数据"""
        with open(self.file, encoding=encoding, mode='w') as f:
            return yaml.dump(data, stream=f, allow_unicode=True)


config = os.path.abspath(os.path.join(os.path.dirname(__file__), "../Config/config.yaml"))
conf = yaml_handler(config).read_yaml()["conf"]
mysql = yaml_handler(config).read_yaml()["mysql"]

variable = os.path.abspath(os.path.join(os.path.dirname(__file__), "../TestCase/test_data/{0}".format(conf['variable'])))
var = yaml_handler(variable).read_yaml()["local_variable"]

if __name__ == '__main__':
    pass
