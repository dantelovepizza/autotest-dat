import json
import re
from common.op_log import error_log, info_log
import random
import string

from common.op_request import My_request
from common.op_yaml import var


def randoms(sub: int):
    if type(sub) == int:
        s = string.digits + string.ascii_letters
        return ''.join(random.choices(s, k=sub))
    else:
        raise TypeError("参数类型不正确，请输入有效整数类型")


def rand_phone():
    pefixlist = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151", "152",
                 "153", "155", "156", "157", "158", "159", "186", "187", "188"]
    return random.choice(pefixlist) + "".join(random.choice("0123456789") for i in range(8))


# 参数化数据替换
def data_handle(sub1, sub2, taget, dicts):
    mark = r'[{0}](.*?)[{1}]'.format(sub1, sub2)
    if sub1 in taget:
        x = re.compile(mark)
        c = x.findall(taget)
        for s in c:
            taget = taget.replace(
                r"{0}{1}{2}".format(sub1, s, sub2), str(dicts[s]))
    return taget


# 获取json数据信息，参考格式：['result', 'msg', '-1', 'status']
def _data_get(dic, locators, default=None):
    """
    :param dic: 输入需要在其中取值的原始字典 <dict>
    :param locators: 输入取值定位器, 如:['result', 'msg', '-1', 'status'] <list>
    :param default: 进行取值中报错时所返回的默认值 (default: None)
    :return: 返回根据参数locators找出的值
    """
    if not isinstance(dic, dict) or not isinstance(locators, list):
        return default
    value = None
    for locator in locators:
        if not type(value) in [dict, list] and isinstance(
                locator, str) and not _can_convert_to_int(locator):
            try:
                value = dic[locator]
            except KeyError:
                return default
            continue
        if isinstance(value, dict):
            try:
                value = _data_get(value, [locator])
            except KeyError:
                return default
            continue
        if isinstance(value, list) and _can_convert_to_int(locator):
            try:
                value = value[int(locator)]
            except IndexError:
                return default
            continue
        if isinstance(value, list) and '[' in locator:
            try:
                i = list_locator(value, locator)
                value = value[i]
            except IndexError:
                return default
            continue
    return value


def list_locator(ls, locator):
    mark = r'[{0}](.*?)[{1}]'.format(r"[", r"=")
    mark2 = r'[{0}](.*?)[{1}]'.format(r"=", r"]")
    x = re.compile(mark)
    k = x.findall(locator)[0]
    x1 = re.compile(mark2)
    v = x1.findall(locator)[0]
    for i in range(len(ls)):
        if isinstance(ls[i][k], str) and v in ls[i][k]:
            return i
        elif eval(v) == ls[i][k]:
            return i
    raise TypeError("定位参数不正确")


def _can_convert_to_int(inputs):
    try:
        int(inputs)
        return True
    except BaseException:
        return False


# 响应参数
def depend_param(locator, response):
    """
    :param response:接口响应请求响应转dict
    :param locator: 待提取参数定位的dict,格式：{"待提取参数":"定位器"}
    :return:params接口响应定位的参数
    """
    params = {}
    if not isinstance(locator, dict) or not isinstance(response, dict):
        error_log.error("定位器或响应体有误")
    for k, y in locator.items():
        locators = y.split(r'/')
        param = _data_get(response, locators)
        params[k] = param
    return params


# 依赖参数化处理：获取响应体中依赖参数，并保存在depend:dict中
def dependence(items, r, depend: dict):
    if items:
        _locators = json.loads(items)
        try:
            param = depend_param(_locators, json.loads(r.text))
            info_log.info(param)
            depend.update(param)
        except Exception as e:
            error_log.error(e)


# 参数化处理：接口传参，由Tester预置参数，一般未随机参数，保证每次运行用例时传参不重复
# 参数暂存放在 \TestCase\test_data\variable.yaml 文件中
def local_variable(var_data: dict):
    for k, v in var.items():
        if "rand" in v:
            var_data[k] = eval(v)
        else:
            var_data[k] = v
    return var_data


if __name__ == '__main__':
    DEPENDENCE = {}
    s = '{"applyListId": "data/evs/add/[resourceContent=evsUPN]/applyListId"}'
    header = {"Cookie": "JSESSIONID=D22D26B170E896E743630DB47A6797DC"}
    from common.op_request import My_request

    req = My_request()
    r = req.run("get", "http://192.168.101.89:18081/applylist/listApplyListsByOperatorId", headers=header)
    d = r.text
    dependence(s, r, DEPENDENCE)
    print(DEPENDENCE)

