.. _intro-overview:

====
概览
====

该项目实现了基于 `Scrapy`_ 的爬虫功能，用于爬取知乎日报文章，供 `MoEar`_ 使用。

对于 `MoEar`_ 来说，并不强求爬虫插件使用何种技术实现，只要符合 `moear-api-common`_
中定义的相关接口即可。


安装方法
========

您可以通过 ``pip`` 进行安装，本包仅在 ``Python 3.X`` 下测试通过::

    pip install moear-spider-zhihudaily


.. _MoEar: https://github.com/littlemo/moear
.. _Scrapy: https://github.com/scrapy/scrapy
.. _Celery: https://github.com/celery/celery
