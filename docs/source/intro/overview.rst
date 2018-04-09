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


业务流程
========

爬虫注册
--------

`MoEar`_ 在启动阶段会加载所有 ``moear.spider`` 扩展插件，并通过调用其
:meth:`.ZhihuDaily.register` 方法获取到该爬虫的配置信息，并持久化到 DB 中。

.. attention::

    注意此方法会在 `MoEar`_ 每次启动时进行调用并更新配置，故在 DB 中修改相应值是没有意义的，
    DB 中的数据仅作为前端显示用（未出现的值不算，如：``enabled``，控制爬虫是否开启）

当前包的注册方法返回值用例，仅供参考::

    {
        'name': 'zhihu_daily',
        'display_name': '知乎日报',
        'author': '小貘',
        'email': 'moore@moorehy.com',
        'description': '每天三次，每次七分钟。在中国，资讯类移动应用的人均阅读时长是 5 分钟，而在知乎日报，这个数字是 21',
        'meta': {
            'crawl_schedule': '0 23 * * *',
            'crawl_random_delay': '3600',
            'package_module': 'mobi',
            'language': 'zh-CN',
            'book_mode': 'periodical',
            'img_cover': '/path/to/moear_spider_zhihudaily/assets/images/cv_zhihudaily.jpg',
            'img_masthead': '/path/to/moear_spider_zhihudaily/assets/images/mh_zhihudaily.gif',
            'image_filter': '["zhihu.com/equation"]',
            'css_package': '/path/to/moear_spider_zhihudaily/assets/css/package.css'
        }
    }

字段说明
~~~~~~~~

name
    *唯一*，作为存储到 DB 中数据模型的主键

display_name
    *唯一*，作为书籍打包时的书籍名称显示

author
    作为书籍打包时的作者显示，少年，留下你的大名吧，让每位阅读者都瞻仰一秒钟~~

email
    邮箱地址，作为 `MoEar`_ 显示数据，方便联系到爬虫作者，提交 Bug

description
    文章源描述，作为 `MoEar`_ 显示数据

meta
    为用于控制爬取计划&打包业务的元数据

    crawl_schedule
        爬取计划任务，遵循标准 `crontab`_ 语法格式

    crawl_random_delay
        爬取任务随机延时最大时间，单位秒。会在 ``0`` 到该值间获取一个随机数值作为爬取前的延时。

        主要考虑到防止被文章源服务器 Ban 掉 IP ，
        故在定点爬取计划任务触发后，再增加指定范围内的随机延时，以保安全。

    package_module
        指定该爬虫爬取的文章在打包时使用的打包模块名，如此处值为 ``mobi`` ，即 `MoEar`_
        会遍历 ``moear.package`` 入口中的 ``mobi`` 插件。作为打包工具传入文章数据列表

    language
        用于指定在生成书籍文件时指定的语言

    book_mode
        书籍模式，针对 **Kindle** 目前支持两种模式，``periodical`` 与 ``book``

        #. periodical，期刊模式支持列表与宫格图的索引显示，但由于官方没有完整的说明文档，
            故很多功能的实现只能靠猜。。。
        #. book，书籍模式，官方有提供完整的用例，故支持较好，但没有索引显示，智能看蹩脚的目录

    img_cover
        当前文章的封面图文件路径，若为空，则使用 `moear-api-common`_ 中提供的默认图片

    img_masthead
        当前文章的报头图文件路径，若为空，则使用 `moear-api-common`_ 中提供的默认图片

    image_filter
        图片链接过滤器，用以将无法被前方设置的 ``package_module``
        打包工具本地化处理的图片过滤掉，避免影响本地化业务执行效率。

        如：当前知乎日报中就会存在公式图片，这些图片是前端生成的，而非静态文件，故会下载异常，
        通过过滤器将其滤掉。

        内容为 ``JSON`` 格式的列表，支持正则表达式

    css_package
        文章的样式文件路径，这就很关键了(雾)，最终打包出来的书籍中排版是否精美全靠它！
        此处建议直接根据文章源前端中的样式设计进行移植，剔除掉 **kindle** 不支持的样式。


.. _MoEar: https://github.com/littlemo/moear
.. _Scrapy: https://github.com/scrapy/scrapy
.. _moear-api-common: https://github.com/littlemo/moear-api-common
.. _Celery: https://github.com/celery/celery
.. _Crontab: https://zh.wikipedia.org/wiki/Cron
