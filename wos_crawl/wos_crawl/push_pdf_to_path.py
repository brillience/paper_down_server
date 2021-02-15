#!/home/zxb/workspace/paper_down_server/venv/bin/python
# -*- coding: utf-8 -*-
# @Time : 2021/2/4 15:14
# @Author : ZhangXiaobo
# @Software: PyCharm

"""
说明：
    每2个小时，扫描pdf所在文件夹下的所有pdf文件
    将文件路径，更新到数据库中paper_server表的path：/static/PDF/file_name.pdf
"""

import os
from model import get_engine, get_session
from model.models import Papers
from sqlalchemy import and_

if __name__ == '__main__':
    pdf_list = os.listdir(r'/home/zxb/store/PDF')
    engine = get_engine()
    session = get_session(engine)

    for pdf in pdf_list:
        file_name = pdf.split('.')[0]
        paper = session.query(Papers).filter(Papers.unique_id == file_name).first()
        if paper.path is None:
            paper.path = '/static/PDF/' + pdf
            session.commit()

    # 将web_url不为空，但是path为空的文献的web_url置为空，方便爬虫程序扫描到，重新爬取
    paper_list = session.query(Papers).filter(and_(Papers.path==None,Papers.web_url!=None)).all()
    for paper in paper_list:
        paper.web_url = None
        session.commit()

    # 将失败的web_url纠正
    paper_list = session.query(Papers).filter(Papers.web_url!=None).all()
    for paper in paper_list:
        if 'cyber' in paper.web_url:
            paper.web_url = None
            paper.path = None
            session.commit()


    session.close()
