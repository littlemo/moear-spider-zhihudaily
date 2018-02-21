# -*- coding: utf-8 -*-
import scrapy


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

    def parse(self, response):
        pass
