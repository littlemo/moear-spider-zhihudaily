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
