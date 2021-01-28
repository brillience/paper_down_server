#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/1/14 16:57
# @Author : ZhangXiaobo
# @Software: PyCharm
# 文献爬取
import logging

import pymysql
import requests
from lxml import etree

class Crawler(object):
    def __init__(self):
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'zh-CN,zh;q=0.9',
            'sec-fetch-dest': 'document',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
            'referer': 'https://www.sci-hub.shop/',
            'origin': 'https://www.sci-hub.shop'
        }
        self.base_url = 'https://www.sci-hub.tf/'
        self.conn = pymysql.connect(user='root',
                                    password='zhang111',
                                    host='127.0.0.1',
                                    port=3306,
                                    database='doi_web_server'
                                    )
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
                create table if not exists doi_url(
                id int primary key auto_increment,
                doi varchar(255) not null,
                url varchar(255) not null 
            );
            """)

    def query(self, doi):
        """
        从数据库中查询资源地址，若不存在，则去爬取，同时保存在数据库
        :param:doi
        :return:pdf_url
        """
        self.doi = doi
        query_sql = "select url from doi_url where doi='{}';".format(self.doi)
        self.cursor.execute(query_sql)
        res = self.cursor.fetchall()
        if res is None or len(res) == 0:
            url = self.get_pdf_url()
            return url
        else:
            return res[0]
        pass

    def get_pdf_url(self):
        """
        爬取pdf_url成功则返回url，同时保存到数据库；失败返回None；
        :return: pdf_url
        """
        data = data = {
            'sci-hub-plugin-check': '',
            'request': self.doi
        }
        response = requests.post(url=self.base_url, data=data, headers=self.headers)
        tree = etree.HTML(response.text)
        pdf_url_list = tree.xpath('//iframe[@id="pdf"]/@src')
        if len(pdf_url_list) == 0:
            logging.error("None pdf_url's " + 'doi:' + self.doi + ' ' + 'request_url:' + response.request.url)
            return None
        else:
            url = pdf_url_list[0].split('#')[0]
            if 'https' not in url:
                url = 'https:' + url
            insert_sql = "INSERT INTO doi_url(doi,url) VALUES(%s,%s);"
            self.cursor.execute(insert_sql, (self.doi, url))
            self.conn.commit()
            return url

    def __del__(self):
        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':
    print(Crawler().query('/10.1089/ast.2019.2067'))
