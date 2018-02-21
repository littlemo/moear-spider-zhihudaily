# -*- coding: utf-8 -*-
import scrapy
import datetime


class ZhihuDailySpider(scrapy.Spider):
    # 来源名称，唯一，长度<255，用于文章源模型索引创建后不可修改
    name = 'zhihu_daily'

    # 显示名称，长度<255，Spider每次运行时更新
    display_name = "知乎日报"

    # 组件作者，Spider每次运行时更新
    author = "小貘"

    # 组件作者邮箱，Spider每次运行时更新
    email = "moore@moorehy.com"

    # 描述信息，长度无限制，Spider每次运行时更新
    description = "每天三次，每次七分钟。在中国，资讯类移动应用的人均阅读时长是 5 分钟，而在知乎日报，这个数字是 21"

    allowed_domains = ['zhihu.com']

    def __init__(self, date=None, *args, **kwargs):
        """
        知乎日报爬虫类，用于爬取&解析知乎日报页面&相关协议
        :param date:  爬取日期，命令行参数，默认为空，即爬取当日最新，内容格式：yyyymmdd
        """
        super(ZhihuDailySpider, self).__init__(*args, **kwargs)

        self.start_urls = ['http://news-at.zhihu.com/api/4/news/latest']

        # 此处由于知乎日报的协议为爬取指定日期的前一天
        # 故需要将Spider接受的date日期+1天作为爬取参数
        if date is not None:
            self.logger.info('指定爬取参数：date={}'.format(date))
            try:
                spider_date = datetime.datetime.strptime(date, '%Y%m%d')
                spider_date += datetime.timedelta(days=1)
                spider_date_str = spider_date.strftime('%Y%m%d')
                self.logger.info(
                    '格式化后的知乎爬取日期参数：{}'.format(spider_date_str))
                self.start_urls = [
                    'http://news.at.zhihu.com/api/4/news/before/{}'.format(
                        spider_date_str)]
            except ValueError:
                self.logger.error('指定的爬取日期错误(yyymmdd)：{}'.format(date))
                self.start_urls = []

    def parse(self, response):
        pass
