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

    def __init__(self, unique_id=None, title=None, authors=None, year=None, month=None, journal=None,
                 doi=None, document_type=None, web_url=None, path=None):
        super(Papers, self).__init__()
        self.unique_id = unique_id
        self.title = title
        self.authors = authors
        self.year = year
        self.month = month
        self.journal = journal
        self.doi = doi
        self.document_type = document_type
        self.web_url = web_url
        self.path = path

    def __repr__(self):
        return '文章ID:{}，标题:{},doi:{}'.format(self.unique_id, self.title, self.doi)

    pass


def push_bib_to_db(bib_papers: list):
    """
    bib_papers的元素是一个字典
    从字典中取出需要的信息，并更新到数据库
    :param bib_papers:
    :return:
    """
    for element in bib_papers:
        try:
            paper = Papers(unique_id=element.get('unique-id').strip(),
                           title=element.get('title') if 'title' in element else None,
                           authors=str(element.get('author') if 'author' in element else None),
                           year=element.get('year') if 'year' in element else None,
                           month=element.get('month') if 'month' in element else None,
                           journal=element.get('journal').lower() if 'journal' in element else None,
                           doi=element.get('doi') if 'doi' in element else None,
                           document_type=element.get('ENTRYTYPE') if 'ENTRYTYPE' in element else None
                           )
            # 先判断数据库中没有该文章，然后再增加进入
            if Papers.query.filter_by(unique_id=paper.unique_id).first() is None:
                db.session.add(paper)
                db.session.commit()
        except Exception as e:
            print('ERROR:', str(e))
            print(element)
    pass
