import sys
import logging
import unittest

from moear_spider_zhihudaily import entry


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
format = logging.Formatter("%(asctime)s - %(message)s")  # output format
sh = logging.StreamHandler(stream=sys.stdout)  # output to standard output
sh.setFormatter(format)
log.addHandler(sh)


class TestSpiderEntryMethods(unittest.TestCase):
    """
    测试爬虫入口类的接口方法

    .. attention::

        此测试将实际发出爬取请求，故会涉及到真是网络请求
    """
    def test_000_register(self):
        """测试注册方法"""
        rc = entry.ZhihuDaily().register()
        log.info(rc)
        self.assertIsInstance(rc, dict)
        for item in rc.values():
            self.assertIsNotNone(item)

    def test_200_format(self):
        """测试文章列表格式化方法"""
        data = [
            {"origin_url": "http://daily.zhihu.com/story/9671902", "title": "大误 · 《舌尖上的中国之：吸血鬼》", "content": "fake data", "spider": "zhihu_daily", "meta": [{"value": 9671902, "name": "spider.zhihu_daily.id"}, {"value": "https://pic4.zhimg.com/v2-0c332103f9b14622a3c3ef5f495901df.jpg", "name": "moear.cover_image_slug"}], "date": "2018-03-04 00:00:00", "author": "终月冥"},
            {"origin_url": "http://daily.zhihu.com/story/9671499", "title": "为什么游戏玩不过我们会一直玩，学习学不明白就不学了？", "content": "fake data", "spider": "zhihu_daily", "meta": [{"value": 9671499, "name": "spider.zhihu_daily.id"}, {"value": 1, "name": "spider.zhihu_daily.top"}, {"value": "https://pic2.zhimg.com/v2-11ee3463d0d3461f046ff95b5c339fa9.jpg", "name": "moear.cover_image_slug"}], "date": "2018-03-04 00:00:00", "author": "暗涌"},
            {"origin_url": "http://daily.zhihu.com/story/9671681", "title": "圆周率里会出现你的银行卡密码吗？", "content": "fake data", "spider": "zhihu_daily", "meta": [{"value": 9671681, "name": "spider.zhihu_daily.id"}, {"value": 1, "name": "spider.zhihu_daily.top"}, {"value": "https://pic3.zhimg.com/v2-1822222b9cac964fccf2d19876933d6e.jpg", "name": "moear.cover_image_slug"}], "date": "2018-03-04 00:00:00", "author": "vortex"},
            {"origin_url": "http://daily.zhihu.com/story/9672093", "title": "本周热门精选 · 人生荒废指北", "content": "fake data", "spider": "zhihu_daily", "meta": [{"value": 9672093, "name": "spider.zhihu_daily.id"}, {"value": 1, "name": "spider.zhihu_daily.top"}, {"value": "https://pic3.zhimg.com/v2-6f6132eea92e4b10729bd1326ce260e2.jpg", "name": "moear.cover_image_slug"}], "date": "2018-03-04 00:00:00", "author": "编辑部小李"},
            {"origin_url": "http://daily.zhihu.com/story/9672023", "title": "有哪些曾经很火，现在却被发现是很危险的发明？", "content": "fake data", "spider": "zhihu_daily", "meta": [{"value": 9672023, "name": "spider.zhihu_daily.id"}, {"value": 1, "name": "spider.zhihu_daily.top"}, {"value": "https://pic3.zhimg.com/v2-532f361cb6cd77dd232696c0177d412a.jpg", "name": "moear.cover_image_slug"}], "date": "2018-03-04 00:00:00", "author": "丁香医生"},
            {"origin_url": "http://daily.zhihu.com/story/9671626", "title": "对方充错话费给我，却要我还？", "content": "fake data", "spider": "zhihu_daily", "meta": [{"value": 9671626, "name": "spider.zhihu_daily.id"}, {"value": "https://pic3.zhimg.com/v2-54d36dbd969829e0c606827b921fb582.jpg", "name": "moear.cover_image_slug"}], "date": "2018-03-04 00:00:00", "author": "TEDCJK，北京儒德律师事务所"},
            {"origin_url": "http://daily.zhihu.com/story/9671926", "title": "瞎扯 · 如何正确地吐槽", "content": "fake data", "spider": "zhihu_daily", "meta": [{"value": 9671926, "name": "spider.zhihu_daily.id"}, {"value": "https://pic1.zhimg.com/v2-8c6c38c1cc3c995d16c864e700d4745c.jpg", "name": "moear.cover_image_slug"}], "date": "2018-03-04 00:00:00", "author": "丶且听风吟，杨络绎，圭多达莱佐，匿名用户"}
        ]
        rc = entry.ZhihuDaily().format(data)
        log.info(rc)
        self.assertIsInstance(rc, dict)
        self.assertIn('热文', rc.keys())
        self.assertIn('文章', rc.keys())
