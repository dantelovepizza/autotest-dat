import json
import os
import time

import traceback
import unittest
from unittest import SkipTest

import requests
from ddt import ddt, data

from common.op_res_variable import data_handle, local_variable, dependence
from common.op_excel import ExcelHandler
from common.op_request import My_request
from common.op_log import error_log, info_log
from common.op_yaml import conf, var

DEPENDENCE = local_variable(var)
session = {}
# 获取测试数据，数据格式:[{'no': 1, 'module': '登录'},{'no': 2, 'module': '登录2'}]
# 读取yaml配置文件，获取excel的sheet名称
# 读取yaml配置文件，查找待运行的EXCEL
sheets, file, base_url = conf['suite'], conf['excel'], conf['base_url']

path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../TestCase/test_data/{0}".format(file)))
cases = ExcelHandler(path).read_excel(sheets)


def get_session(req):
    cookie = {'Cookie': 'JSESSIONID=' +
                        requests.utils.dict_from_cookiejar(req.session.cookies).get('JSESSIONID')}
    return cookie


def req_format(req, items):
    formats = "\n用例名称：{6}\n" \
              "测试步骤：{7}\n" \
              "请求URL：{5}:{3}\n" \
              "请求头：{4}\n" \
              "返回状态码：{1}\n" \
              "响应头：{0}\n" \
              "响应体：{2}\n" \
        .format(req.headers, req.status_code, req.json(), req.url, req.request.headers, req.request.method,
                items['TC_Cases'], items['TC_STEP'])
    return formats


# 是否延时
# 隐式等待/显示等待设计
def wait(times):
    try:
        if times and type(times) is int:
            time.sleep(times)
            info_log.info("wait {}s".format(times))
    except Exception as e:
        error_log.error("{}".format(traceback.format_exc()))
        raise e


@ddt
class Run_TestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.req = My_request()
        self.header = {}
        self.params = None
        self.path_url = None
        self.requests_data = None

    def tearDown(self) -> None:
        self.req.session_close()

    @data(*cases)
    def test_RunCase(self, items):
        # 必须先设置用例名称和测试步骤，否则报告可能会因为获取不到测试用例名而无法分类，会出现错乱
        self._testMethodName = items['TC_Cases']
        self._testMethodDoc = items['TC_STEP']  # HtmlTestRunner报告显示的用例名称
        self.data_check(items)
        # 执行接口请求
        try:
            r = self.req.run(
                method=items['method'],
                content_type=items['content_type'],
                url=base_url + self.path_url,
                payload=self.requests_data,
                headers=self.header, params=self.params)
            r_formats = req_format(r, items)
            info_log.info(msg=r_formats)
            print(r_formats)
        except Exception as e:
            error_log.error("{0}-{1}请求异常：{2}".format(self._testMethodName, self._testMethodDoc, traceback.format_exc()))
            raise e
        self.assert_case(items, r)
        dependence(items['depend_locator'], r, DEPENDENCE)
        wait(items['sleep'])

    def assert_case(self, items, r):
        try:
            self.assertEqual(r.json()['code'], int(items['except_code']))
            self.assertIn(items['except_msg'], str(r.text))
            if 'Login' in items['TC_STEP']:
                print(get_session(self.req))
                session.update(get_session(self.req))
                print(session)
        except AssertionError as e:
            error_log.error("{0}-{1}断言失败：{2}".format(self._testMethodName, self._testMethodDoc, traceback.format_exc()))
            raise e

    def data_check(self, items):
        # 是否跳过执行
        if items['skip']:
            raise SkipTest("跳过此步骤:{}".format(str(items['skip'])))
        # 检查Url中是否包含路径参数：items['url']是否包含{param}字段。如果有，则在dependence字典中查找依赖字典
        if items['url'] is None:
            error_log.error(self.name + "url输入有误！")
        elif '{' in items['url']:
            self.path_url = data_handle("{", "}", items['url'], DEPENDENCE)
        else:
            self.path_url = items['url'].strip()

        # header是否有传值，如有则追加到header。
        if items['header']:
            self.header.update(json.loads(items['header']))
        self.header.update(session)
        # 查询参数拼接，参数以 {'k':'v'}方式传入
        if items['query']:
            params = ''
            query_param = eval(items['query'])
            for k, v in query_param.items():
                params += r"{0}={1}&".format(k, v)
            self.path_url = self.path_url + f"?{params.rstrip('&')}"

        # data参数：目前有{key:values},[values],参数化使用&param&替换。
        if items['data']:
            try:
                if "&" in items['data']:
                    self.requests_data = eval(data_handle("&", "&", items['data'], DEPENDENCE))
                else:
                    self.requests_data = eval(items['data'])
            except Exception as e:
                error_log.error(
                    "{0}-{1} 请求参数异常\n：{2}".format(self._testMethodName, self._testMethodDoc, traceback.format_exc()))
                raise e
        if items['except_code'] and items['except_msg']:
            if '&' in items['except_msg']:
                items['except_msg'] = data_handle("&", "&", items['except_msg'], DEPENDENCE)
        else:
            error_log.error("Error:断言信息不能为空")


if __name__ == '__main__':
    unittest.main()
