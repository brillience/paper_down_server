#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/2/22 18:50
# @Author : ZhangXiaobo
# @Software: PyCharm
"""
生成app，用于uwsgi部署
"""

from app import create_app
app = create_app('production')
