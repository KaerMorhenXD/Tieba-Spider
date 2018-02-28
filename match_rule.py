"""
    匹配规则
"""

import re


class Singleton(object):
    """
        单例模式
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance


class RegexMatch(Singleton):
    """
        正则匹配所需内容
    """

    def __init__(self):
        pass

    def post_url(self, html):
        """
            匹配帖子链接
        :return: url list
        """
        pattern = re.compile(
            r'<a rel="noreferrer"\s+href="/(p/\d+)" title=".*?" target="_blank" class="j_th_tit ">.*?</a>')
        return pattern.findall(html)

    def post_total_pages(self, html):
        """
            匹配每一篇帖子内的总页数
        :return type: int
        """
        pattern = re.compile(r'<a href="/p/.*?\?pn=(.*?)">尾页</a>')
        page_number = pattern.findall(html)
        page_number = int(page_number[0]) if page_number else 1
        return page_number

    def img_url(self, html):
        """
            匹配每篇帖子每页的图片 url
        :return: url list
        """
        pattern = re.compile(r'<img class="BDE_Image" src="(.*?)".*?>')
        return pattern.findall(html)
