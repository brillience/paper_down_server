#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/1/28 17:18
# @Author : ZhangXiaobo
# @Software: PyCharm

"""
    后端需要的表单信息（将需要的表单，单独列出，便于清晰使用）
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class QueryForm(FlaskForm):
    """
    表单类，用于前端输入检索式
    """
    query = StringField('请输入web of science任意合法的检索式', validators=[DataRequired()])
    submit = SubmitField('search')
    pass
