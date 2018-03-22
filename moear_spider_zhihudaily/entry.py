import os
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
    """
    知乎日报爬虫插件
    """
    def hook_custom_options(self):
        """
        配置定制配置项钩子
        ------------

        该方法返回当前类的自定义配置项，由基类在 ``__init__`` 方法中调用，
        调用点位于，Common默认全局配置完成后，用户元数据配置前

        :returns: dict, 返回当前类的自定义配置项
        """
        return {}

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
                'package_module': 'mobi',
                'language': 'zh-CN',
                'book_mode': 'periodical',  # 'periodical' | 'book'
                'img_cover': os.path.join(
                    _images_path, 'cv_zhihudaily.jpg'),
                'img_masthead': os.path.join(
                    _images_path, 'mh_zhihudaily.gif'),
                'image_filter': ['equation\?tex='],
                'css_package': os.path.join(
                    _css_path, 'package.css')
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
            crawler = CrawlerScript()
            crawler.crawl(output_file=temp.name)

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
        sections = OrderedDict()
        hot_list = []
        normal_list = []
        for item in data:
            meta_dict = {}
            meta = item.get('meta', [])
            for m in meta:
                for (k, v) in m.items():
                    meta_dict[m['name']] = m.get('value')

            # 如果标题为空，则迭代下一条目
            if not item.get('title'):
                continue

            # 处理文章摘要，若为空则根据正文自动生成并填充
            if not item.get('excerpt') and item.get('content'):
                soup = BeautifulSoup(item.get('content'), "lxml")
                word_limit = self.options.get(
                    'toc_desc_word_limit', 500)
                content_list = soup.select('div.content')
                content_list = [content.get_text() for content in content_list]
                excerpt = ' '.join(content_list)[:word_limit]
                item['excerpt'] = excerpt

            # 从item中提取出section分组
            top = meta_dict.pop('spider.zhihu_daily.top', '0')
            item['meta'] = meta_dict
            if str(top) == '1':
                hot_list.append(item)
            else:
                normal_list.append(item)

        if hot_list:
            sections.setdefault('头条', hot_list)
        if normal_list:
            sections.setdefault('日报', normal_list)
        return sections
