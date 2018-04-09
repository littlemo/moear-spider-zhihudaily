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
