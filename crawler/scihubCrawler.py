#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/1/14 16:57
# @Author : ZhangXiaobo
# @Software: PyCharm
# 文献爬取
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
        self.proxies = None
        try:
            proxy = requests.get("http://127.0.0.1:5010/get/").json().get("proxy")
            self.proxies = {"http": "http://{}".format(proxy)}
            pass
        except:
            pass

    def query(self, doi):
        """
        从数据库中查询资源地址，若不存在，则去爬取
        :param:doi
        :return:pdf_url
        """
        self.doi = doi
        url = self.get_pdf_url()
        return url

    def get_pdf_url(self):
        """
        爬取pdf_url成功则返回url；失败返回None；
        :return: pdf_url
        """
        data = {
            'sci-hub-plugin-check': '',
            'request': self.doi
        }
        if self.proxies is None:
            response = requests.post(url=self.base_url, data=data, headers=self.headers)
        else:
            response = requests.post(url=self.base_url, data=data, headers=self.headers, proxies=self.proxies)
        tree = etree.HTML(response.text)
        pdf_url_list = tree.xpath('//iframe[@id="pdf"]/@src')
        if len(pdf_url_list) == 0:
            return None
        else:
            url = pdf_url_list[0].split('#')[0]
            if 'https' not in url:
                url = 'https:' + url
            return url


if __name__ == '__main__':
    print(Crawler().query('/10.1089/ast.2019.2067'))
