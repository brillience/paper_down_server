#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/1/28 17:17
# @Author : ZhangXiaobo
# @Software: PyCharm
import os
from flask import render_template, request, flash

from crawler.scihubCrawler import Crawler
from . import main
from .forms import QueryForm
from ..models import Papers,db
from ..models import push_bib_to_db

os.path.join('...')


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
            return render_template('query_res.html', papers=bib_dic_list,sum=len(bib_dic_list))

    return render_template('index.html', form=form)
    pass


@main.route('/submit', methods=['POST'])
def submit():
    """
    1、查询数据库中是否存在该path；若不存在，调用scihub获取url；若存在path，将本地的path转为url的形式。
    2、以字典的形式返回，客户端需要进行分页处理和打包下载
    :return:
    """
    papers_dic_succ_list = []
    papers_dic_err_list = []
    unique_id_list = request.form.getlist('unique_id')
    for unique_id_ in unique_id_list:
        url = None
        paper = Papers.query.filter_by(unique_id=unique_id_).first()
        if paper.path is None:
            if paper.web_url is None:
                paper.web_url = Crawler().query(paper.doi)
                url = paper.web_url
        else:
            # 注意path的格式需为httpid
            url = paper.path
        paper_ = {
            'title': paper.title,
            'doi': paper.doi,
            'url': url,
            'file_name': unique_id_
        }
        if url is None:
            papers_dic_err_list.append(paper_)
        else:
            papers_dic_succ_list.append(paper_)

    return render_template('down_page.html', papers_dic_succ_list=papers_dic_err_list,
                           papers_dic_err_list=papers_dic_err_list)
