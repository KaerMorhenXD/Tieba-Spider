from urllib import request, parse
import re

# https://tieba.baidu.com/f?ie=utf-8&kw=P站fr=search
root_url = "http://tieba.baidu.com/"

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "zh,zh-CN;q=0.9",
    "Host": "tieba.baidu.com",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36",
}

words = {
    "ie": "utf-8",
    "kw": "P站",
    "fr": "search",
}

kw = parse.urlencode(words)

# 构造请求贴吧地址
tieba_url = root_url + "f?" + kw
print(tieba_url)

# 构造下一页地址
# https://tieba.baidu.com/f?kw=p%E7%AB%99&ie=utf-8&pn=50
next_word = {
    "kw": "p站",
    "ie": "utf-8",
    "pn": "100",
}
next_kw = parse.urlencode(next_word)
next_url = root_url + "f?" + next_kw
print(next_url)

# 加载页面，获取网页源码
req = request.Request(next_url, headers=headers)
response = request.urlopen(req)
html_text = response.read().decode('utf-8')
print(html_text)

# 匹配帖子标题
pattern_title = re.compile(
    r'<a rel="noreferrer"\s+href="/p/\d+" title=".*?" target="_blank" class="j_th_tit ">(.*?)</a>')
title_list = pattern_title.findall(html_text)
print(title_list)
print(len(title_list))

# 匹配帖子链接
pattern_title_link = re.compile(
    r'<a rel="noreferrer"\s+href="/(p/\d+)" title=".*?" target="_blank" class="j_th_tit ">.*?</a>')
title_link_list = pattern_title_link.findall(html_text)
print(title_link_list)
print(len(title_link_list))

# 匹配评论数
pattern_comment_nums = re.compile(r'<span class="threadlist_rep_num center_text"\s*title="回复">(.*?)</span>')
comment_nums_list = pattern_comment_nums.findall(html_text)
print(comment_nums_list)
print(len(comment_nums_list))


class TiebaSpider(object):
    """
        贴吧爬虫: 爬取帖子，评论数，帖子链接，贴内所有图片
    """
    def __init__(self):
        self.tieba = input("请输入需要爬取的贴吧名：")
        self.root_url = "http://tieba.baidu.com/"
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "zh,zh-CN;q=0.9",
            "Host": "tieba.baidu.com",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36",
        }

    def start_page(self):
        words = {
            "ie": "utf-8",
            "kw": self.tieba,
            "fr": "search",
        }
        kw = parse.urlencode(words)

        # 构造请求贴吧地址
        tieba_url = self.root_url + "f?" + kw
        print(tieba_url)

    def next_page(self, page):
        # 构造下一页地址
        # https://tieba.baidu.com/f?kw=p%E7%AB%99&ie=utf-8&pn=50
        next_word = {
            "kw": self.tieba,
            "ie": "utf-8",
            "pn": page,
        }
        next_kw = parse.urlencode(next_word)
        next_url = root_url + "f?" + next_kw
        print(next_url)

    def load_page(self):
        # 加载页面，获取网页源码
        req = request.Request(next_url, headers=self.headers)
        response = request.urlopen(req)
        html_text = response.read().decode('utf-8')
        print(html_text)

    def get_post_info(self):
        # 匹配帖子标题
        pattern_title = re.compile(
            r'<a rel="noreferrer"\s+href="/p/\d+" title=".*?" target="_blank" class="j_th_tit ">(.*?)</a>')
        title_list = pattern_title.findall(html_text)
        print(title_list)
        print(len(title_list))

        # 匹配帖子链接
        pattern_title_link = re.compile(
            r'<a rel="noreferrer"\s+href="/(p/\d+)" title=".*?" target="_blank" class="j_th_tit ">.*?</a>')
        title_link_list = pattern_title_link.findall(html_text)
        print(title_link_list)
        print(len(title_link_list))

        # 匹配评论数
        pattern_comment_nums = re.compile(r'<span class="threadlist_rep_num center_text"\s*title="回复">(.*?)</span>')
        comment_nums_list = pattern_comment_nums.findall(html_text)
        print(comment_nums_list)
        print(len(comment_nums_list))
