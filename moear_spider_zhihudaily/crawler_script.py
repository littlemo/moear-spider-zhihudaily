from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from billiard import Process
from . import settings as config


class CrawlerScript():

    def __init__(self):
        settings = Settings()
        settings.setmodule(config)
        self.crawler = CrawlerProcess(settings)

    def _crawl(self, *args, **kwargs):
        self.crawler.crawl('zhihu_daily', *args, **kwargs)
        self.crawler.start()
        self.crawler.stop()

    def crawl(self, *args, **kwargs):
        p = Process(target=self._crawl, args=args, kwargs=kwargs)
        p.start()
        p.join()
