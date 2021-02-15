#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/2/2 11:22
# @Author : ZhangXiaobo
# @Software: PyCharm
from sqlalchemy import Column, String, Integer

from . import Base


class Papers(Base):
    __tablename__ = 'papers'
    unique_id = Column(String(20), primary_key=True)
    title = Column(String(500), index=True)
    authors = Column(String(500))
    year = Column(Integer)
    month = Column(String(10))
    journal = Column(String(255))
    doi = Column(String(255), index=True)
    document_type = Column(String(50))
    web_url = Column(String(255))
    path = Column(String(100))

    def __repr__(self):
        return '文章ID:{}，标题:{},doi:{}'.format(self.unique_id, self.title, self.doi)
