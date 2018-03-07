import tempfile

from moear_spider_common import base
from .zhihudaily.spiders.zhihu_daily \
    import ZhihuDailySpider as zhihu
from .crawler_script import CrawlerScript


class ZhihuDaily(base.SpiderBase):
    """
    知乎日报爬虫插件
    """

    def register(self, *args, **kwargs):
        """
        注册
        ----

        调用方可根据主键字段进行爬虫的创建或更新操作

        :returns: dict, 返回符合接口定义的字典数据
        """
        return {
            'name': zhihu.name,
            'display_name': zhihu.display_name,
            'author': zhihu.author,
            'email': zhihu.email,
            'description': zhihu.description,
            'meta': {
                'package': 'mobi',
                'package_support': [
                    'mobi',
                ],
            }
        }

    def crawl(self, *args, **kwargs):
        """
        爬取
        ----

        执行爬取操作，并阻塞直到爬取完成，返回结果数据

        :returns: json, 返回符合接口定义的JSON包字符串
        """
        temp = tempfile.NamedTemporaryFile(mode='w+t')

        try:
            print('temp.name => {}'.format(temp.name))
            crawler = CrawlerScript(temp.name)
            crawler.crawl()

            temp.seek(0)
            content = temp.read()
        finally:
            temp.close()

        print('抓取完毕！')
        return content

    def format(self, data, *args, **kwargs):
        """
        格式化
        ------

        将传入的Post列表数据进行格式化处理

        :param data: 待处理的文章列表
        :type data: list

        :returns: dict, 返回符合mobi打包需求的定制化数据结构
        """
        pass
