#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/1/28 17:17
# @Author : ZhangXiaobo
# @Software: PyCharm
"""
    后后端视图函数：
        index（主页）[GET POST]
        submit（提交文献表单）[POST]
        download（单个文件下载）[GET]
        downloadall（批量文件下载）[POST]
"""
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
    """
    GET：显示主页
    POST：提交表单（检索式），爬取wos，将结果返回前端
    :return:检索结果 或 主页
    """
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

            # 此处需要先得到检索的结果
            # 若篇数大于1000篇，提示用户去wos修正检索式，保证文章数目<=1000
            # 若满足，则再去拿取结果
            from crawler.requests_wos import WosCrawler
            crawler = WosCrawler(query_str=query_str)
            paper_num = crawler.get_papers_num()
            if paper_num <= 1000 and paper_num > 0:
                bib_tex = crawler.get_bibtex()
                from bibtex_parser.bibtex_parser import parse_bib_str
                bib_dic_list = parse_bib_str(bib_tex)
                push_bib_to_db(bib_dic_list)
                # 此处前端，需要取出各个元素的文献信息
                return render_template('query_res.html', papers=bib_dic_list, sum=len(bib_dic_list))
            elif paper_num==0:
                info = '检索结果文章数目为0篇，请前往 <a href="http://www.webofknowledge.com/">web of science</a>  修改检索式！'
                return render_template('query_err_info.html',info=info)
            else:
                info= '检索结果文章数目超出1000篇，请前往 <a href="http://www.webofknowledge.com/">web of science</a>  修改检索式！'
                return render_template('query_err_info.html',info=info)

    return render_template('index.html', form=form)
    pass


# 提交选中的文献
@main.route('/submit', methods=['POST'])
def submit():
    """
    1、查询数据库中是否存在该path；若不存在，则返回失败的表格；若存在path，将本地的path转为url的形式。
    2、以字典的形式返回，客户端需要进行分页处理和打包下载
    :return:渲染下载页面
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
    """
    单个文件下载
    :param filename:
    :return:单个文献下载
    """
    return send_from_directory('./static/PDF', filename,
                               as_attachment=True)  # as_attachment=True 一定要写，不然会变成打开，而不是下载
    pass


# 打包下载
@main.route('/downloadall', methods=['POST'])
def download_all():
    """
    POST：提交文献的unique_id，将对应的若干个文献，在内存中打包，实现一个压缩包的下载
    :return:压缩包下载
    """
    id_list = request.form.getlist('ids')
    memory_file = BytesIO()
    with zipfile.ZipFile(memory_file, 'a', zipfile.ZIP_DEFLATED) as zf:
        pathes = [os.path.join(main.root_path, 'app/static/PDF/') + id + '.pdf' for id in id_list]
        for path in pathes:
            with open(path, 'rb') as fp:
                zf.writestr(path.split('static')[-1], fp.read())
    memory_file.seek(0)

    return send_file(memory_file,
                     attachment_filename='papers.zip',
                     as_attachment=True)
