import requests
from requests.adapters import HTTPAdapter

from common.op_res_variable import *

"""
重写request要解决的问题：
1.超时设置
2.错误重试
3.请求响应耗时
4.设置公共请求头
5.post form/json
6.调用接口日志
"""


class My_request:
    def __init__(self, timeout=8):
        self.session = requests.Session()
        #: 在session实例上挂载Adapter实例, 目的: 请求异常时,自动重试
        self.session.mount('http://', HTTPAdapter(max_retries=3))
        self.session.mount('https://', HTTPAdapter(max_retries=3))
        #: 设置为False, 主要是HTTPS时会报错, 为了安全也可以设置为True
        self.session.verify = False
        #: 公共的请求头设置
        self.session.headers = {
        }
        #: 挂载到self上面
        self.timeout = timeout

        # 根据EXCEL的datatype字段选择post参数类型form/json

    def run(self, method, url, content_type=None, params=None, payload=None,
            headers=None, **kwargs):
        if content_type is None:
            return self.session.request(method, url, params=params, headers=headers, **kwargs)
        if content_type == 'json':
            return self.session.request(method, url, params=params, json=payload, headers=headers, **kwargs)
        if content_type == 'form':
            return self.session.request(method, url, params=params, data=payload, headers=headers, **kwargs)

    def cookies(self):
        return requests.utils.dict_from_cookiejar(self.session.cookies)

    def session_close(self):
        self.session.close()


if __name__ == '__main__':
    # s = {"username":"admin","password":"da0dfc69961c482dbb1c453917a8066b"}
    # req = My_request()
    # # header = {'Cookie': 'JSESSIONID=669929C0B6EA1E34E89D01BD24BEAD23', 'Content-Length': '0'}
    # r = req.run("post", "http://hxdmc.cn/cas/v1/tickets", content_type='form', payload=s)
    # # print(type((r.json()["data"]['evs']['change'][0])))
    # r1 = req.run("get","http://hxdmc.cn?ticket=ST-54-VKt7npsoorFgdu5joIh2K4BpAPo-hxyy-cas-serverrc-4jcqt",)
    # print(r1.request.headers)
    pass
