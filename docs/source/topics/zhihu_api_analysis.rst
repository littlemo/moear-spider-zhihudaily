.. _topics-zhihu-api-analysis:

===========
知乎API分析
===========

声明
====

.. hint::

    以下知乎日报协议分析主要参考于 `知乎日报 API 分析 <https://github.com/izzyleung/ZhihuDailyPurify/wiki/知乎日报-API-分析>`_ ，针对于部分协议进行了额外的验证和补充，以及实际爬取的逻辑阐述，侵删

.. important::

    感谢 ``Xiao Liang`` 前辈的贡献 Orz，正愁无门路打算直接硬抓Web版文章信息的时候，
    看到您的这篇分析文章，如醍醐灌顶一般，整个人瞬间精神了！


API 说明
========

* 本协议分析主要针对于知乎日报第 ``4`` 版 API，且主要关注于文章相关内容获取部分，
  其余更全面的部分，如：启动界面、软件版本、评论相关、主题日报等 APP 相关协议可参考上述链接

* 以下所有 API 使用的 HTTP Method 均为 ``GET``


API 分析
========

最新消息
--------

请求链接
~~~~~~~~

**GET** ``http://news-at.zhihu.com/api/4/news/latest``

响应实例
~~~~~~~~

::

    {
        "date": "20161201",
        "stories": [{
            "images": ["http://pic1.zhimg.com/1336c8a5e842c11912014f093cc69d58.jpg"],
            "type": 0,
            "id": 9026396,
            "ga_prefix": "120111",
            "title": "收了的税全部返还，民众福利怎么就大大下降了？"
        }
        ...
        ],
        "top_stories": [{
            "image": "http://pic4.zhimg.com/8fc4831c28432f700b6400de882fd833.jpg",
            "type": 0,
            "id": 9022827,
            "ga_prefix": "120113",
            "title": "爱看《冰与火之歌》和《魔戒》，没想到背后这么多八卦"
        },
        ...
        ]
    }

字段分析
~~~~~~~~

date
    日期

stories
    当日新闻

    title
        新闻标题

    images
        图像地址（官方 API 使用数组形式。目前暂未有使用多张图片的情形出现，**曾见无** ``images`` **属性的情况** ，请在使用中注意 ）

    ga_prefix
        供 Google Analytics 使用

    type
        作用未知

    id
        ``url`` 与 ``share_url`` 中最后的数字（应为内容的 id）

    multipic
        消息是否包含多张图片（仅出现在包含多图的新闻中）

top_stories
    界面顶部 ViewPager 滚动显示的显示内容（子项格式同上）（请注意区分此处的 ``image`` 属性与 ``stories`` 中的 ``images`` 属性）

补充信息
~~~~~~~~

#. ``images`` 字段不存在的情况，如：`《8 月 1 日，这些新闻值得你了解一下》 <http://daily.zhihu.com/story/4065555>`_ ，获取到的列表项内容为::

    {
        "type": 0,
        "id": 4065555,
        "ga_prefix": "010115",
        "title": "8 月 1 日，这些新闻值得你了解一下"
    }

#. ``top_stories.image`` 字段中的图片为APP中的顶部轮播图使用，故分辨率会比 ``stories`` 中的相同文章块 ``images`` 里的图片拥有更高的分辨率，一般情况下，前者为 ``640*640``，而后者仅为 ``150*150``。故在做文章爬取时可以根据实际需求进行选择，下节将说明如何获取非热文的高质量封面图
