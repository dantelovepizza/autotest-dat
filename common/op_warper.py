import time
from functools import *
from common.op_log import info_log


# 将request请求详情发送到info日志
def request_log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        t1 = time.time()
        r = func(*args, **kwargs)
        t = time.time() - t1  # 请求耗时
        # 请求参数
        formats = "请求耗时={4:0.2f}s\n" \
                  "请求路径：{3}\n" \
                  "请求头：{0}\n" \
                  "返回状态码：{1}\n" \
                  "响应头：{5}\n" \
                  "响应体：{2}\n" \
            .format(r.headers, r.status_code, r.json(), r.url, t, r.request.headers)
        info_log.info(msg=formats)
        return func(*args, **kwargs)
    return wrapper


if __name__ == '__main__':
    pass
