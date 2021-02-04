import requests
import scrapy
from scrapy import Request
from ..items import WosCrawlItem
from ..model import get_engine, get_session
from ..model.models import Papers
import re


class WosSpiderSpider(scrapy.Spider):
    name = 'wos_spider'
    def start_requests(self):
        self.engine = get_engine()
        self.session = get_session(engine=self.engine)
        # 获取scihub资源链接
        paper_list = self.session.query(Papers).filter(Papers.web_url == None).all()
        for paper in paper_list:
            if paper.doi is None:
                continue
            proxy = requests.get("http://127.0.0.1:5010/get/").json().get("proxy")
            detail_url = 'https://www.sci-hub.ren/' + paper.doi
            yield Request(url=detail_url,dont_filter=True,
                              meta={'proxy': "http://{}".format(proxy), 'unique_id':paper.unique_id}, callback=self.parse)
            pass

    def parse(self, response):
        detail_url_list = response.xpath('//*[@id="buttons"]/ul/li[2]/a/@onclick')
        if len(detail_url_list) > 0:
            target = detail_url_list.extract_first()
            find_url = re.compile(r"href='(.*?)'")
            target_url = re.findall(find_url, target)[0]
            if target_url[0] != 'h':
                target_url = 'https:' + target_url
            if "\\" in target_url:
                target_url = target_url.replace('\\', '')
            # 更新web_url
            self.session.query(Papers).filter(Papers.unique_id==response.meta['unique_id']).update({'web_url':target_url})
            self.session.commit()

            item = WosCrawlItem()
            item['file_urls'] = []
            item['file_urls'].append(target_url)
            item['name']=response.meta['unique_id']
            yield item


        pass
