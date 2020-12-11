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

    def run(self, method, url, content_type=None, params=None, data=None,
            headers=None, **kwargs):
        if content_type is None:
            return self.session.request(method, url, params=params, headers=headers, **kwargs)
        if method.lower() == 'post' and content_type == 'json':
            return self.session.request(method, url, params=params, json=data, headers=headers, **kwargs)
        if method.lower() == 'post' and content_type.lower() == 'form':
            return self.session.request(method, url, params=params, data=data, headers=headers, **kwargs)

    def cookies(self):
        return requests.utils.dict_from_cookiejar(self.session.cookies)

    def session_close(self):
        self.session.close()


if __name__ == '__main__':
    # reqs = My_request()
    # # ';'.join([headers['cookie'], ['='.join(i) for i in r.cookies.items()]])
    # data = {"applyId": "", "azoneId": "495ce550-a285-41eb-9345-26404597da79", "azoneName": "vmware_cinder",
    #         "azoneLabelName": "v8_cinder", "hostName": "cpn-v8rc@vmware_volume",
    #         "businessSystemId": "f4fead37-27ab-4fe6-b2a7-109335b417c0", "businessSystemName": "0722测试1",
    #         "volumeName": "volumeNam", "description": "", "volumeNums": 1, "serverId": "", "serverName": "",
    #         "shared": "false", "storageType": "普通", "newVolumeSize": "", "normId": "", "oldVolumeSize": "",
    #         "resTenancy": "-1", "volumeSize": 100}
    # r = reqs.run(
    #     method="Post",
    #     content_type="json",
    #     url="http://192.168.101.89:18081/serverApply/volume",
    #     data=data,
    #     headers={'Cookie': 'JSESSIONID=063AD7E12599F236FE8F505C7BC7FFF3'}, params=None)
    #
    # print(r.request.headers)
    pass