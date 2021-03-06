#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/1/25 19:43
# @Author : ZhangXiaobo
# @Software: PyCharm
"""
采用requests对wos进行发起检索请求，抓取检索结果
使用：
    1、获取文章数量 get_papers_num
    2、拿取检索结果 get_bibtex
"""
import time

import re
import requests
from lxml import etree

HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Connection': 'keep-alive'
}


class WosCrawler(object):
    """
    web of science爬虫
    提交表单数据，拿到该网站后台的检索结果（也就是bibtex格式的文档）
    """

    def __init__(self, query_str: str):
        """
        1、打开网页
        2、提交检索式
        query 为检索式 ： TS  TI  AU 支持任意合法的检索式
        :param query_str:
        """

        self.query_str = query_str
        self.sid = None
        self.qid = None
        # sid qid 是提交表单数据的必要信息
        self.db_list = []
        self.base_url = 'http://www.webofknowledge.com/'
        self.bibtext = ''
        self.paper_num = 0
        self.entry_url = ''  # 结果入口链接

        self._open_page()
        self._submit_query()


    def _open_page(self):
        """
        打开网页，提取 sid 和 已购买的数据库
        :return:
        """
        response = requests.get(url=self.base_url, headers=HEADERS)
        tree = etree.HTML(response.text)
        # 提取sid
        self.sid = re.search(r'SID=(\w+)&', response.url).group(1)
        # 提取已购买的数据库
        db_str = tree.xpath("//select[@id='ss_showsuggestions']/@onchange")[0]
        db_pattern = r'WOS\.(\w+)'
        self.db_list = re.findall(db_pattern, db_str)

    def _submit_query(self):
        """
        提交表单，提取结果入口链接、提取qid、提取文章数量
        :return:
        """
        adv_search_url = 'http://apps.webofknowledge.com/WOS_AdvancedSearch.do'
        query_form = {
            "product": "WOS",
            "search_mode": "AdvancedSearch",
            "SID": self.sid,
            "input_invalid_notice": "Search Error: Please enter a search term.",
            "input_invalid_notice_limits": " <br/>Note: Fields displayed in scrolling boxes must be combined with at least one other search field.",
            "action": "search",
            "replaceSetId": "",
            "goToPageLoc": "SearchHistoryTableBanner",
            "value(input1)": self.query_str,
            "value(searchOp)": "search",
            "value(select2)": "LA",
            "value(input2)": "",
            "value(select3)": "DT",
            "value(input3)": '',
            "value(limitCount)": "14",
            "limitStatus": "collapsed",
            "ss_lemmatization": "On",
            "ss_spellchecking": "Suggest",
            "SinceLastVisit_UTC": "",
            "SinceLastVisit_DATE": "",
            "period": "Range Selection",
            "range": "ALL",
            "startYear": "1900",
            "endYear": time.strftime('%Y'),
            "editions": self.db_list,
            "update_back2search_link_param": "yes",
            "ss_query_language": "",
            "rs_sort_by": "PY.D;LD.D;SO.A;VL.D;PG.A;AU.A",
        }
        # 提交查询表单
        response = requests.post(url=adv_search_url, data=query_form, headers=HEADERS)
        tree = etree.HTML(response.text)
        # 提取结果入口的链接
        # 当检索到为空时，没有链接入口
        try:
            self.entry_url = tree.xpath("//a[@id='hitCount']/@href")[0]
            self.entry_url = 'http://apps.webofknowledge.com' + self.entry_url
            qid_pattern = r'qid=(\d+)&'
            self.qid = re.search(qid_pattern, self.entry_url).group(1)
            self.paper_num = int(tree.xpath("//a[@id='hitCount']/text()")[0].replace(',', ''))
        except:
            self.paper_num=0

    def _get_bibtex(self):
        """
        获取bibtex格式的文档的内容
        :return:
        """
        if self.paper_num==0:
            return None
        response = requests.get(url=self.entry_url, headers=HEADERS)
        # 一次只能拿到500条结果
        span = 500
        # 计算需要导出的次数
        iter_num = self.paper_num // span + 1
        for i in range(1, iter_num + 1):
            end = i * span
            start = (i - 1) * span + 1
            if end > self.paper_num:
                end = self.paper_num
            output_form = {
                "selectedIds": "",
                "displayCitedRefs": "true",
                "displayTimesCited": "true",
                "displayUsageInfo": "true",
                "viewType": "summary",
                "product": "WOS",
                "rurl": response.url,
                "mark_id": "WOS",
                "colName": "WOS",
                "search_mode": "AdvancedSearch",
                "locale": "en_US",
                "view_name": "WOS-summary",
                "sortBy": "PY.D;LD.D;SO.A;VL.D;PG.A;AU.A",
                "mode": "OpenOutputService",
                "qid": str(self.qid),
                "SID": str(self.sid),
                "format": "saveToFile",
                "filters": "PMID AUTHORSIDENTIFIERS ACCESSION_NUM ISSN CONFERENCE_SPONSORS CONFERENCE_INFO SOURCE TITLE AUTHORS",
                "mark_to": str(end),
                "mark_from": str(start),
                "queryNatural": str(self.query_str),
                "count_new_items_marked": "0",
                "use_two_ets": "false",
                "IncitesEntitled": "no",
                "value(record_select_type)": "range",
                "markFrom": str(start),
                "markTo": str(end),
                "fields_selection": "PMID AUTHORSIDENTIFIERS ACCESSION_NUM ISSN CONFERENCE_SPONSORS CONFERENCE_INFO SOURCE TITLE AUTHORS",
                "save_options": 'bibtex'
            }
            output_url = 'http://apps.webofknowledge.com//OutboundService.do?action=go&&'
            response = requests.post(url=output_url, data=output_form, headers=HEADERS)
            #  WoS的bibtex格式不规范，需要特别处理一下
            bibtext_temp = response.text.replace('Early Access Date', 'Early-Access-Date').replace('Early Access Year',
                                                                                                   'Early-Access-Year')
            # 将结果整合
            self.bibtext = self.bibtext + bibtext_temp

    def get_papers_num(self):
        return self.paper_num

    def get_bibtex(self):
        self._get_bibtex()
        return self.bibtext

if __name__ == '__main__':
    crawler = WosCrawler(query_str='TS=(doiomite) AND PY=(2020)')
    paper_nums = crawler.get_papers_num()
    if paper_nums==0:
        print('检索结果文章数目为0篇，请前往',crawler.base_url,'的高级检索中确定检索式！')
    elif paper_nums<=1000:
        print(crawler.get_bibtex())
    else:
        print('检索结果文章数目超出1000篇，请前往',crawler.base_url,'的高级检索中确定检索式！')
