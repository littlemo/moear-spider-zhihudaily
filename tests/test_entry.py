import os
import sys
import json
import logging
import unittest

from moear_api_common import utils
from moear_spider_zhihudaily import entry


log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
format = logging.Formatter("%(asctime)s - %(message)s")  # output format
sh = logging.StreamHandler(stream=sys.stdout)  # output to standard output
sh.setFormatter(format)
log.addHandler(sh)

_base_dir = os.path.dirname(os.path.abspath(__file__))
_build_dir = os.path.join(_base_dir, '..', 'moear_spider_zhihudaily', 'build')


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

    def test_100_crawl(self):
        rc = entry.ZhihuDaily().crawl()
        data = json.dumps(rc, ensure_ascii=False)
        utils.mkdirp(_build_dir)
        with open(os.path.join(_build_dir, 'crawl.json'), 'w') as fh:
            fh.write(data)
        log.debug(rc)

    def test_200_format(self):
        """测试文章列表格式化方法"""
        with open(os.path.join(_build_dir, 'crawl.json'), 'r') as fh:
            data_json = fh.read()
        data = json.loads(data_json, encoding='UTF-8')
        rc = entry.ZhihuDaily().format(data)
        log.debug(rc)
        with open(os.path.join(_build_dir, 'format.py'), 'w') as fh:
            fh.write(str(rc))
        self.assertIsInstance(rc, dict)
        self.assertIn('热闻', rc.keys())
        self.assertIn('日报', rc.keys())
