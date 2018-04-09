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


项目结构
========

包路径说明如下::

    .
    ├── __init__.py
    ├── assets                      # 资产路径，用来存储当前文章源的静态资源
    │   ├── css
    │   │   └── package.css         # 为打包时提供的该文章源的文章样式文件
    │   └── images
    │       ├── cv_zhihudaily.jpg   # 为打包时提供的书籍封面，600*800
    │       └── mh_zhihudaily.gif   # 为打包时提供的书籍报头，600*60
    ├── crawler_script.py           # 用于提供可程序调用Scrapy的爬行类
    ├── entry.py                    # 实现接口定义的入口文件
    ├── items.py                    # Scrapy 的数据模型
    ├── middlewares.py              # Scrapy 的中间件
    ├── pipelines.py                # Scrapy 的流水线
    ├── settings.py                 # Scrapy 的参数设置
    └── spiders                     # Scrapy 的具体爬虫实现路径
        ├── __init__.py
        └── zhihu_daily.py          # 知乎日报的爬虫主体


.. _MoEar: https://github.com/littlemo/moear
.. _Scrapy: https://github.com/scrapy/scrapy
.. _moear-api-common: https://github.com/littlemo/moear-api-common
.. _Celery: https://github.com/celery/celery
