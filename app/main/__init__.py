#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/1/28 17:16
# @Author : ZhangXiaobo
# @Software: PyCharm

"""
创建app所需要的所有蓝图
"""

from flask import Blueprint

main = Blueprint('main', '__name__')

from . import views, errors
