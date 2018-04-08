from setuptools import setup, find_packages

root_pack = 'moear_spider_zhihudaily.entry'


setup(
    name='moear-spider-zhihudaily',
    url='https://github.com/littlemo/moear-spider-zhihudaily',
    author='moear developers',
    author_email='moore@moorehy.com',
    maintainer='littlemo',
    maintainer_email='moore@moorehy.com',
    version='1.0.0',
    description='MoEar扩展爬虫功能插件 - 知乎日报',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    keywords='moear scrapy',
    packages=find_packages(exclude=('docs', 'build', 'tests*')),
    include_package_data=True,
    zip_safe=False,
    license='GPLv3',
    python_requires='>=3',
    project_urls={
        'Documentation': 'http://moear-spider-zhihudaily.rtfd.io/',
        'Source': 'https://github.com/littlemo/moear-spider-zhihudaily',
        'Tracker':
            'https://github.com/littlemo/moear-spider-zhihudaily/issues',
    },
    install_requires=[
        'beautifulsoup4~=4.6.0',
        'billiard~=3.5.0.3',
        'moear-api-common~=1.0.0',
        'Scrapy~=1.5.0',
    ],
    entry_points={
        'moear.spider': [
            'zhihu_daily = {}:ZhihuDaily'.format(root_pack),
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: MacOS X',
        'Framework :: Scrapy',
        'Framework :: Twisted',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: Chinese (Simplified)',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Communications :: Email',
        'Topic :: Documentation :: Sphinx',
        'Topic :: Internet',
        'Topic :: Software Development :: Version Control :: Git',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Networking',
        'Topic :: Terminals',
        'Topic :: Utilities',
    ],
)
