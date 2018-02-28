import random
import time
import requests
from urllib import parse

from TiebaCrawler_v2.proxy import get_response
from TiebaCrawler_v2.match_rule import RegexMatch


class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance


class Crawler(Singleton):
    """
        抓取类：用来抓取各种所需信息
    """

    def __init__(self, tieba, start_page, end_page, post_queue, img_queue):
        self.root_url = "http://tieba.baidu.com/"
        self.url = "http://tieba.baidu.com/f?"
        self.tieba = tieba
        self.start_page = start_page
        self.end_page = end_page
        self.post_queue = post_queue
        self.img_queue = img_queue
        self.regex_match = RegexMatch()

    def tieba_next_page(self):
        """
            生成指定页数的贴吧 url 列表并返回
        :return: url list
        """
        url_list = []
        for page in range(self.start_page, self.end_page + 1):
            pn = (page - 1) * 50
            kw = {
                "kw": self.tieba,
                "ie": "utf-8",
                "pn": pn,
            }
            word = parse.urlencode(kw)
            url = self.url + word
            url_list.append(url)

        print(url_list)
        return url_list

    def post_url(self, url):
        """
            获取贴吧指定页数内，所有帖子的链接地址
        :return: url list
        """

        html = get_response(url=url).text

        # 获取当前页所有帖子 url 列表
        post_url_list = []
        url_list = self.regex_match.post_url(html)
        for u in url_list:
            post_url_list.append(self.root_url + u)

        print("帖子url:", end="")
        print(post_url_list)
        return post_url_list

    def post_page_url(self, url):
        """
            得到该帖子的总页数
            用页数构建每一页的 url 列表，并返回
        :return: url list
        """
        html = get_response(url).text

        # 匹配得到页数
        post_total_pages = self.regex_match.post_total_pages(html)
        print("该帖子共" + str(post_total_pages) + "页")

        # 利用页数构造每页的 url
        post_page_url_list = []
        for pn in range(post_total_pages):
            post_page_url_list.append(url + "?pn=" + str(pn + 1))

        return post_page_url_list

    def img_url(self, url):
        """
            获取帖子内所有图片链接
        :return:
        """
        html = get_response(url).text

        # 获取该页下所有图片 url 列表
        img_url_list = self.regex_match.img_url(html)
        print("图片url:", end="")
        print(img_url_list)

        return img_url_list
