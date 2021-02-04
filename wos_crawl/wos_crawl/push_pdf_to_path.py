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
