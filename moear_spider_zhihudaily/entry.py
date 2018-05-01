import os
import json
import html
import tempfile
from collections import OrderedDict

from bs4 import BeautifulSoup

from moear_api_common import base
from .spiders.zhihu_daily import ZhihuDailySpider as zhihu
from .crawler_script import CrawlerScript


_base_dir = os.path.dirname(os.path.abspath(__file__))
_assets_dir = os.path.join(_base_dir, 'assets')
_images_path = os.path.join(_assets_dir, 'images')
_css_path = os.path.join(_assets_dir, 'css')


class ZhihuDaily(base.SpiderBase):
    '''
    知乎日报爬虫插件
    '''
    def hook_custom_options(self):
        '''
        该方法返回当前类的自定义配置项，由基类在 ``__init__`` 方法中调用，
        调用点位于，Common默认全局配置完成后，用户元数据配置前

        :return: 返回当前类的自定义配置项
        :rtype: dict
        '''
        return {}

    def register(self, *args, **kwargs):
        '''
        调用方可根据主键字段进行爬虫的创建或更新操作

        :return: 返回符合接口定义的字典数据
        :rtype: dict
        '''
        return {
            'name': zhihu.name,
            'display_name': zhihu.display_name,
            'author': zhihu.author,
            'email': zhihu.email,
            'description': zhihu.description,
            'meta': {
                # 爬取计划，参考 crontab 配置方法
                'crawl_schedule': '0 23 * * *',

                # 执行爬取的随机延时，单位秒，用于避免被 Ban
                'crawl_random_delay': str(60 * 60),

                'package_module': 'mobi',
                'language': 'zh-CN',
                'book_mode': 'periodical',  # 'periodical' | 'book'
                'img_cover': os.path.join(
                    _images_path, 'cv_zhihudaily.jpg'),
                'img_masthead': os.path.join(
                    _images_path, 'mh_zhihudaily.gif'),
                'image_filter': json.dumps(['zhihu.com/equation']),
                'css_package': os.path.join(
                    _css_path, 'package.css')
            }
        }

    def crawl(self, *args, **kwargs):
        '''
        执行爬取操作，并阻塞直到爬取完成，返回结果数据。
        此处考虑到 Scrapy 本身的并发特性，故通过临时文件方式做数据传递，
        将临时路径传递到爬虫业务中，并在爬取结束后对文件进行读取、 JSON 反序列化，返回

        :return: 返回符合接口定义的字典对象
        :rtype: dict
        '''
        temp = tempfile.NamedTemporaryFile(mode='w+t')

        try:
            crawler = CrawlerScript()
            # 调试时可指定明确日期参数，如：date='20180423'
            crawler.crawl(output_file=temp.name)

            temp.seek(0)
            content = json.loads(temp.read(), encoding='UTF-8')
        finally:
            temp.close()

        print('抓取完毕！')
        return content

    def format(self, data, *args, **kwargs):
        '''
        将传入的Post列表数据进行格式化处理。此处传入的 ``data`` 格式即为
        :meth:`.ZhihuDaily.crawl` 返回的格式，但具体内容可以不同，即此处保留了灵活度，
        可以对非当日文章对象进行格式化，制作相关主题的合集书籍

        :param data: 待处理的文章列表
        :type data: list

        :return: 返回符合mobi打包需求的定制化数据结构
        :rtype: dict
        '''
        sections = OrderedDict()
        hot_list = []
        normal_list = []
        for item in data:
            meta = item.get('meta', [])

            # 如果标题为空，则迭代下一条目
            if not item.get('title'):
                continue

            soup = BeautifulSoup(item.get('content'), "lxml")

            # 清洗文章内容，去除无用内容
            for view_more in soup.select('.view-more'):
                view_more.extract()
            item['content'] = str(soup.div)

            # 处理文章摘要，若为空则根据正文自动生成并填充
            if not item.get('excerpt') and item.get('content'):
                word_limit = self.options.get(
                    'toc_desc_word_limit', 500)
                content_list = soup.select('div.content')
                content_list = [content.get_text() for content in content_list]
                excerpt = ' '.join(content_list)[:word_limit]
                # 此处摘要信息需进行HTML转义，否则会造成toc.ncx中tag处理错误
                item['excerpt'] = html.escape(excerpt)

            # 从item中提取出section分组
            top = meta.pop('spider.zhihu_daily.top', '0')
            item['meta'] = meta
            if str(top) == '1':
                hot_list.append(item)
            else:
                normal_list.append(item)

        if hot_list:
            sections.setdefault('热闻', hot_list)
        if normal_list:
            sections.setdefault('日报', normal_list)
        return sections
