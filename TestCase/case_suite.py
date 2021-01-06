"""
要解决的问题
1.测试用例分级别运行：P1冒烟测试、P2主流程测试例、P3全流程测试例、P4异常场景测试例、P5参数类型/边界值/必填校验测试例。
（测试EXCEL文档TC_Cases配置）
2.测试用例分模块运行：config中suite配置
"""
Level = {
    'P1': 1,
    'P2': 2,
    'P3': 3,
    'P4': 4,
    'P5': 5,
}


# 根据config.yaml筛选用例级别
def catch_level(level):
    """
    :param level: 读取用例级别,P1-P5
    :return: 返回用例级别列表
    """
    if isinstance(level, str) and level in Level:
        _level = [k for k, v in Level.items() if v in (x + 1 for x in range(Level.get(level)))]
        return _level
    else:
        raise KeyError("case_level参数不正确！！！")


# 根据用例级别筛选测试用例
def verify_cases(level, case, key='TC_Cases'):
    """
    :param level: 用例级别
    :param case: EXCEL读取的原始用例集
    :param key: EXCEL筛选字段，默认从'TC_Cases'字段筛选
    :return:
    """
    try:
        cases_list = [i for i in case if i[key][0:2].upper() in level]
        return cases_list
    except KeyError as k:
        raise k
    except Exception as e:
        raise e
