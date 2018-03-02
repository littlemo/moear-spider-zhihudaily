from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from billiard import Process
from .zhihudaily import settings as config


class CrawlerScript():

    def __init__(self, tmp_file):
        settings = Settings()
        settings.setmodule(config)
        settings.set(
            'FEED_URI',
            'file://{file}'.format(file=tmp_file))
        self.crawler = CrawlerProcess(settings)

    def _crawl(self):
        self.crawler.crawl('zhihu_daily')
        self.crawler.start()
        self.crawler.stop()

    def crawl(self):
        p = Process(target=self._crawl)
        p.start()
        p.join()
