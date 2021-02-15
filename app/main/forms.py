#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/1/28 17:18
# @Author : ZhangXiaobo
# @Software: PyCharm
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class QueryForm(FlaskForm):
    query = StringField('请输入web of science任意合法的检索式', validators=[DataRequired()])
    submit = SubmitField('search')
    pass
