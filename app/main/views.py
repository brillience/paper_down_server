#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/1/28 17:17
# @Author : ZhangXiaobo
# @Software: PyCharm
import zipfile

import os

from flask import render_template, request, flash, send_from_directory, send_file
from io import BytesIO


from . import main
from .forms import QueryForm
from ..models import Papers
from ..models import push_bib_to_db

os.path.join('...')



# 输入检索式
@main.route('/', methods=['GET', 'POST'])
def index():
    form = QueryForm()
    if request.method == 'POST' and form.validate():
        if '=' not in form.query.data:
            flash('请输入合法的检索式!')
        else:
            """
            1、将检索式提交wos，获取bibtex检索结果
            2、解析bibtex，将数据库中没有的paper信息添加到数据库
            3、跳转到检索结果页面，渲染页面
            """
            query_str = form.query.data
            from crawler.requests_wos import WosCrawler
            crawler = WosCrawler()
            bib_tex = crawler.query(query_str=query_str)
            from bibtex_parser.bibtex_parser import parse_bib_str
            bib_dic_list = parse_bib_str(bib_tex)
            push_bib_to_db(bib_dic_list)
            # 此处前端，需要取出各个元素的文献信息
            return render_template('query_res.html', papers=bib_dic_list, sum=len(bib_dic_list))

    return render_template('index.html', form=form)
    pass


# 提交选中的文献
@main.route('/submit', methods=['POST'])
def submit():
    """
    1、查询数据库中是否存在该path；若不存在，则返回失败的表格；若存在path，将本地的path转为url的形式。
    2、以字典的形式返回，客户端需要进行分页处理和打包下载
    :return:
    """
    papers_dic_succ_list = []
    papers_dic_err_list = []
    unique_id_list = request.form.getlist('uniqueid')
    for unique_id_ in unique_id_list:
        url = None
        paper = Papers.query.filter_by(unique_id=unique_id_).first()
        if paper.path is None:
            pass
        else:
            # 注意path的格式需为httpid
            url = paper.path
        paper_ = {
            'title': paper.title,
            'doi': paper.doi,
            'url': url,
            'journal': paper.journal,
            'file_name': unique_id_
        }
        if url is None:
            papers_dic_err_list.append(paper_)
        else:
            papers_dic_succ_list.append(paper_)

    return render_template('down_page.html', papers_dic_succ_list=papers_dic_succ_list,
                           num_succ=len(papers_dic_succ_list),
                           num_err=len(papers_dic_err_list),
                           papers_dic_err_list=papers_dic_err_list)


# 文件下载
@main.route("/download/<path:filename>")
def downloader(filename):
    return send_from_directory('./static/PDF', filename,
                               as_attachment=True)  # as_attachment=True 一定要写，不然会变成打开，而不是下载
    pass


# 打包下载
@main.route('/downloadall', methods=['POST'])
def download_all():
    id_list = request.form.getlist('ids')
    memory_file = BytesIO()
    with zipfile.ZipFile(memory_file, 'a', zipfile.ZIP_DEFLATED) as zf:
        pathes = [os.path.join(main.root_path,'app/static/PDF/') + id + '.pdf' for id in id_list]
        for path in pathes:
            with open(path, 'rb') as fp:
                zf.writestr(path.split('static')[-1], fp.read())
    memory_file.seek(0)

    return send_file(memory_file,
                     attachment_filename='papers.zip',
                     as_attachment=True)
