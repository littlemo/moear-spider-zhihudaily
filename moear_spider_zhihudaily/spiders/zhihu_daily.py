# -*- coding: utf-8 -*-
import os
import html
import scrapy
import datetime
import json
from bs4 import BeautifulSoup

from moear_api_common import utils


class ZhihuDailySpider(scrapy.Spider):
    #: 来源名称，唯一，长度<255，用于文章源模型索引创建后不可修改
    name = 'zhihu_daily'

    #: 显示名称，长度<255，Spider每次运行时更新
    display_name = "知乎日报"

    #: 组件作者，Spider每次运行时更新
    author = "小貘"

    #: 组件作者邮箱，Spider每次运行时更新
    email = "moore@moorehy.com"

    #: 描述信息，长度无限制，Spider每次运行时更新
    description = \
        "每天三次，每次七分钟。在中国，资讯类移动应用的人均阅读时长是 5 分钟，" \
        "而在知乎日报，这个数字是 21"

    allowed_domains = ['zhihu.com']

    def __init__(self, date=None, *args, **kwargs):
        """
        知乎日报爬虫类，用于爬取&解析知乎日报页面&相关协议

        :param str date: 爬取日期，命令行参数，默认为空，即爬取当日最新，内容格式：``yyyymmdd``
        :param str output_file: (可选，关键字参数)结果输出文件，
            用以将最终爬取到的数据写入到指定文件中，默认为 ``moear_spider_zhihudaily``
            下的 ``build`` 路径，建议仅作为测试时使用
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

        self.item_list = []
        self.output_file = kwargs.get('output_file', None)
        if not self.output_file:
            # 此处逻辑用于命令行执行 ``scrapy crawl zhihu_daily`` 测试时的文件输出
            _base_dir = os.path.dirname(os.path.dirname(
                os.path.abspath(__file__)))
            _output_file_default = os.path.join(
                _base_dir, 'build', 'output.json')
            utils.mkdirp(os.path.dirname(_output_file_default))
            self.output_file = _output_file_default
        self.logger.info('输出文件路径: {}'.format(self.output_file))

    def parse(self, response):
        '''
        根据对 ``start_urls`` 中提供链接的请求响应包内容，解析生成具体文章链接请求

        :param Response response: 由 ``Scrapy`` 调用并传入的请求响应对象
        '''
        content_raw = response.body.decode()
        self.logger.debug('响应body原始数据：{}'.format(content_raw))
        content = json.loads(content_raw, encoding='UTF-8')
        self.logger.debug(content)

        # 文章发布日期
        date = datetime.datetime.strptime(content['date'], '%Y%m%d')

        strftime = date.strftime("%Y-%m-%d")
        self.logger.info('日期：{}'.format(strftime))

        # 处理头条文章列表，将其 `top` 标记到相应 __story__ 中
        if 'top_stories' in content:
            self.logger.info('处理头条文章')
            for item in content['top_stories']:
                for story in content['stories']:
                    if item['id'] == story['id']:
                        story['top'] = 1
                        break
                self.logger.debug(item)

        # 处理今日文章，并抛出具体文章请求
        post_num = len(content['stories'])
        self.logger.info('处理今日文章，共{:>2}篇'.format(post_num))
        for item in content['stories']:
            self.logger.info(item)
            post_num = 0 if post_num < 0 else post_num
            pub_time = date + datetime.timedelta(minutes=post_num)
            post_num -= 1

            url = 'http://news-at.zhihu.com/api/4/news/{}'.format(item['id'])
            request = scrapy.Request(url, callback=self.parse_post)
            post_dict = {
                'spider': ZhihuDailySpider.name,
                'date': pub_time.strftime("%Y-%m-%d %H:%M:%S"),
                'meta': {
                    'spider.zhihu_daily.id': str(item.get('id', ''))
                }
            }
            if item.get('top'):
                post_dict['meta']['spider.zhihu_daily.top'] = \
                    str(item.get('top', 0))
            request.meta['post'] = post_dict
            self.item_list.append(post_dict)
            yield request

    def parse_post(self, response):
        '''
        根据 :meth:`.ZhihuDailySpider.parse` 中生成的具体文章地址，获取到文章内容，
        并对其进行格式化处理，结果填充到对象属性 ``item_list`` 中

        :param Response response: 由 ``Scrapy`` 调用并传入的请求响应对象
        '''
        content = json.loads(response.body.decode(), encoding='UTF-8')
        post = response.meta['post']

        post['origin_url'] = content.get('share_url', '')
        if not all([post['origin_url']]):
            raise ValueError('原文地址为空')

        post['title'] = html.escape(content.get('title', ''))
        if not all([post['title']]):
            raise ValueError('文章标题为空 - {}'.format(post.get('origin_url')))

        # 单独处理type字段为1的情况，即该文章为站外转发文章
        if content.get('type') == 1:
            self.logger.warn('遇到站外文章，单独处理 - {}'.format(post['title']))
            return post

        soup = BeautifulSoup(content.get('body', ''), 'lxml')
        author_obj = soup.select('span.author')
        self.logger.debug(author_obj)
        if author_obj:
            author_list = []
            for author in author_obj:
                author_list.append(
                    author.string.rstrip('，, ').replace('，', ','))
            author_list = list(set(author_list))
            post['author'] = html.escape('，'.join(author_list))
        post['content'] = str(soup.div)

        # 继续填充post数据
        image_back = content.get('images', [None])[0]
        if image_back:
            post['meta']['moear.cover_image_slug'] = \
                content.get('image', image_back)
        self.logger.debug(post)

    def closed(self, reason):
        '''
        异步爬取全部结束后，执行此关闭方法，对 ``item_list`` 中的数据进行 **JSON**
        序列化，并输出到指定文件中，传递给 :meth:`.ZhihuDaily.crawl`

        :param obj reason: 爬虫关闭原因
        '''
        self.logger.debug('结果列表: {}'.format(self.item_list))

        output_strings = json.dumps(self.item_list, ensure_ascii=False)
        with open(self.output_file, 'w') as fh:
            fh.write(output_strings)
