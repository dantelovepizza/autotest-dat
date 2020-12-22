import requests
from requests.adapters import HTTPAdapter
from common.op_warper import request_log

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

    # def run(self, method, url, content_type=None, params=None, data=None,
    #         headers=None, **kwargs):
    #     if content_type is None:
    #         return self.session.request(method, url, params=params, headers=headers, **kwargs)
    #     if method.lower() == 'post' and content_type == 'json':
    #         return self.session.request(method, url, params=params, json=data, headers=headers, **kwargs)
    #     if method.lower() == 'post' and content_type.lower() == 'form':
    #         return self.session.request(method, url, params=params, data=data, headers=headers, **kwargs)
    #     if method.lower() == 'put' and content_type == 'json':
    #         return self.session.request(method, url, json=data, headers=headers, **kwargs)
    #     if method.lower() == 'put' and content_type == 'data':
    #         return self.session.request(method, url, data=data, headers=headers, **kwargs)
    def run(self, method, url, content_type=None, params=None, payload=None,headers=None, **kwargs):
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
    data = {
    "loginName":"maizi003",
    "password":"YTEzODQzODE5NDM4IQ==",
    "retypePassword":"YTEzODQzODE5NDM4IQ==",
    "userName":"maizi003",
    "gxNumber":"maizi003",
    "email":"maizi003@qq.com",
    "telephone":"13843813333",
    "idType":999,
    "certification":"maizi003",
    "address":"maizi003地址",
    "group1":"1",
    "group":{
        "4":"4",
        "5":"fed291e9843b11eaa5ae0a580af000fb"
    },
    "appIds":[
        "73f3c49a84c34d7eae1138b5555252a7"
    ],
    "reason":"自动测试"
}
    mq = My_request()
    r = mq.run("post", "http://hxdmc.cn/register/user", content_type='json', data=data)
    print(r.text)
    print(r.status_code)