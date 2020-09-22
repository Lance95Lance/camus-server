#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
=================================================
@Project -> File   ：camus-server -> urls
@IDE    ：PyCharm
@Author ：Lance
@Date   ：2020/3/3 8:56 上午
@Desc   ：check readme.md
==================================================
"""

# 导入枚举类
from enum import unique
from utils.rewrite_utils.MyChoiceEnum import ChoiceEnum, MyChoiceEnumUtil


@unique
class CasePriority(ChoiceEnum):
    URGENT = "P0"
    HIGH = "P1"
    MEDIUM = "P2"
    LOW = "P3"


@unique
class CaseStatus(ChoiceEnum):
    NO_EXECUTE = "未执行"
    PASS = "通过"
    FAILED = "失败"
    BLOCK = "阻塞"
    HAND_UP = "挂起"


if __name__ == '__main__':
    print(MyChoiceEnumUtil(CaseStatus).get_key_from_enum_value("P0"))
