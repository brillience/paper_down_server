#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/1/28 16:11
# @Author : ZhangXiaobo
# @Software: PyCharm

from . import db


class Papers(db.Model):
    __tablename__ = 'papers'
    unique_id = db.Column(db.String(20), primary_key=True)
    title = db.Column(db.String(500), index=True)
    authors = db.Column(db.String(500))
    year = db.Column(db.Integer)
    month = db.Column(db.String(10))
    journal = db.Column(db.String(255))
    doi = db.Column(db.String(255), index=True)
    document_type = db.Column(db.String(50))
    web_url = db.Column(db.String(255))
    path = db.Column(db.String(100))

    def __repr__(self):
        return '文章ID:{}，标题:{},doi:{}'.format(self.unique_id, self.title, self.doi)

    pass
