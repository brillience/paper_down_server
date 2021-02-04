# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy import Request
from scrapy.pipelines.files import FilesPipeline
from .model import get_engine,get_session
from .model.models import Papers

class WosCrawlPipeline:
    def open_spider(self,spider):
        self.engine = get_engine()
        self.session = get_session(engine=self.engine)

    def process_item(self, item, spider):
        path = '/PDF/' + item['name'] + '.pdf'
        self.session.query(Papers).filter(Papers.unique_id==item['name']).update({'path':path})
        self.session.commit()
        pass

    def close_spider(self,spider):
        self.session.close()



class fileDown(FilesPipeline):

    def get_media_requests(self, item, info):
        # 向FilesPipline提交url地址，进行文件下载
        self.name = item['name']
        for url in item['file_urls']:
            yield Request(url)

    def file_path(self, request, response=None, info=None):
        file_name = self.name + '.pdf'
        return file_name
