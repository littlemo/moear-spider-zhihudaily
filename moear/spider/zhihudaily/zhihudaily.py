from moear.spider.common import base
from moear_spider_zhihudaily.spiders import zhihu_daily as zhihu

import os
import json
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class ZhihuDaily(base.SpiderBase):
    """
    知乎日报爬虫插件
    """

    def register(self):
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
        }

    def crawl(self):
        """
        爬取
        ----

        执行爬取操作，并阻塞直到爬取完成，返回结果数据

        :returns: dict, 返回符合接口定义的字典数据
        """
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        tmp_file = os.path.join(BASE_DIR, 'test.json')

        # 获取并修改项目设置
        setting = get_project_settings()
        setting.set(
            'FEED_URI',
            'file://{file}'.format(file=tmp_file))

        # 创建爬取处理器
        process = CrawlerProcess(setting)

        if os.path.exists(tmp_file):
            os.remove(tmp_file)
            print('移除已存在的临时文件')
        process.crawl('zhihu_daily')
        process.start()

        with open(tmp_file, 'r') as f:
            rc = f.read()
            content = json.loads(rc, encoding='UTF-8')

        os.remove(tmp_file)
        print('抓取完毕！')
        return content

    def format(self, data):
        """
        格式化
        ------

        将传入的Post列表数据进行格式化处理

        :param data: 待处理的文章列表
        :type data: list

        :returns: dict, 返回符合mobi打包需求的定制化数据结构
        """
        pass
