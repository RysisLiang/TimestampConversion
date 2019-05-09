# -*- coding: utf-8 -*-

import sys
import alfred
import time
import re
from datetime import datetime

_pattern1 = "%Y-%m-%d %H:%M:%S"
_pattern2 = "%Y%m%d %H:%M:%S"
_pattern3 = "%Y/%m/%d %H:%M:%S"
_pattern4 = "%Y.%m.%d %H:%M:%S"
_pattern5 = "%Y-%m-%d"
_pattern6 = "%Y%m%d"
_pattern7 = "%Y/%m/%d"
_pattern8 = "%Y.%m.%d"
_patterns = [_pattern1, _pattern2, _pattern3, _pattern4, _pattern5, _pattern6, _pattern7, _pattern8]


# 时间戳格式化
def _format_by_pattern(time_num, pattern):
    time_stamp = float(time_num / 1000)
    time_array = time.localtime(time_stamp)
    return str(time.strftime(pattern, time_array))


# 解析时间字符串
def _parse_by_pattern(timestr, pattern):
    datetime_obj = datetime.strptime(timestr, pattern)
    return str(int(time.mktime(datetime_obj.timetuple()) * 1000 + datetime_obj.microsecond / 1000))


# 多格式匹配解析
def _parses(timestr, index=0):
    try:
        return _parse_by_pattern(timestr, _patterns[index])
    except Exception:
        if index < len(_patterns):
            index += 1
            return _parses(timestr, index)
        else:
            return None


# 获取指定时间或时间戳
def _getOnce(query):
    result = []
    title = "{}".format(query)
    subtitle = "未匹配到指定格式"

    # 设置alfred-xml item
    def setItem(uid, arg, title, subtitle):
        result.append(alfred.Item(
            {"uid": uid, "arg": arg},
            title,
            subtitle,
            None
        ))

    # 匹配时间戳
    r_res = re.search(r'(^\d{13}$)|(^\d{10}$)', query)
    # 匹配日期的格式
    r2_res = re.search(r'^((\d{4}([-\./]\d{2}){2})|2\d{7})\s*(\d{2}(:\d{2}){2})?', query)

    if r_res and r_res.group():
        time_num = int(query)
        # 处理秒时间戳
        if len(query) == 10:
            time_num = time_num * 1000

        res1 = _format_by_pattern(time_num, _pattern1)
        res2 = _format_by_pattern(time_num, _pattern2)
        subtitle = "[{}]-格式化".format(query)
        setItem(1, res1, res1, subtitle)
        setItem(2, res2, res2, subtitle)
    elif r2_res and r2_res.group():
        res = _parses(query)
        subtitle = "[{}]-解析".format(query)
        setItem(1, res, res, subtitle)
    else:
        setItem(1, title, title, subtitle)

    _out(result)


# 获取当前时间和时间戳
def _getNow():
    nowTime = time.time()
    nowDate = datetime.now()

    t1 = nowDate.strftime(_pattern1)
    t2 = nowDate.strftime(_pattern2)
    t3 = int(nowTime * 1000)
    t4 = int(nowTime)
    result = [
        alfred.Item(
            {"uid": 1, "arg": t1},
            "{}".format(t1),
            "当前时间1",
            None
        ),
        alfred.Item(
            {"uid": 2, "arg": t2},
            "{}".format(t2),
            "当前时间2",
            None
        ),
        alfred.Item(
            {"uid": 3, "arg": t3},
            "{}".format(t3),
            "时间戳（毫秒）",
            None
        ),
        alfred.Item(
            {"uid": 4, "arg": t4},
            "{}".format(t4),
            "时间戳（秒）",
            None
        )
    ]
    _out(result)


# 输出xml
def _out(result):
    alfred.write(alfred.xml(result))


# 引入程序入口
def main(param):
    if param:
        _getOnce(param)
    else:
        _getNow()


# 脚本程序入口
if __name__ == "__main__":
    args = sys.argv
    if len(args) > 1 and args[1]:
        main(args[1])
    else:
        main(None)
    # test
    # main('2019-05-08 10:10:10')
    # main('2019-05-08 10:10:1')
    # main('155731466900')
