from urllib import request, parse
import re
import time
import random

# https://tieba.baidu.com/f?ie=utf-8&kw=P站fr=search
# root_url = "http://tieba.baidu.com/"
#
# headers = {
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
#     "Accept-Language": "zh,zh-CN;q=0.9",
#     "Host": "tieba.baidu.com",
#     "Upgrade-Insecure-Requests": "1",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36",
# }
#
# words = {
#     "ie": "utf-8",
#     "kw": "P站",
#     "fr": "search",
# }
#
# kw = parse.urlencode(words)
#
# # 构造请求贴吧地址
# tieba_url = root_url + "f?" + kw
# print(tieba_url)
#
# # 构造下一页地址
# # https://tieba.baidu.com/f?kw=p%E7%AB%99&ie=utf-8&pn=50
# next_word = {
#     "kw": "p站",
#     "ie": "utf-8",
#     "pn": "100",
# }
# next_kw = parse.urlencode(next_word)
# next_url = root_url + "f?" + next_kw
# print(next_url)
#
# # 帖子链接
# # https://tieba.baidu.com/p/5564081306
# post_link = "https://tieba.baidu.com/p/5564081306"
#
# # 加载页面，获取网页源码
# req = request.Request(post_link, headers=headers)
# response = request.urlopen(req)
# html_text = response.read().decode('utf-8')
# print(html_text)
#
# # 匹配帖子标题
# pattern_title = re.compile(
#     r'<a rel="noreferrer"\s+href="/p/\d+" title=".*?" target="_blank" class="j_th_tit ">(.*?)</a>')
# title_list = pattern_title.findall(html_text)
# print(title_list)
# print(len(title_list))
#
# # 匹配帖子链接
# pattern_title_link = re.compile(
#     r'<a rel="noreferrer"\s+href="/(p/\d+)" title=".*?" target="_blank" class="j_th_tit ">.*?</a>')
# title_link_list = pattern_title_link.findall(html_text)
# print(title_link_list)
# print(len(title_link_list))
#
# # 匹配评论数
# pattern_comment_nums = re.compile(r'<span class="threadlist_rep_num center_text"\s*title="回复">(.*?)</span>')
# comment_nums_list = pattern_comment_nums.findall(html_text)
# print(comment_nums_list)
# print(len(comment_nums_list))
#
# # 获取总页数
# # pattern_all_page_nums = re.compile(
# #     r'<a href="//tieba.baidu.com/f\?kw=.*&pn=(\d*?)" class="last pagination-item " >尾页</a>')
# # all_page_nums = int(pattern_all_page_nums.findall(html_text)[0]) // 50
# # print(all_page_nums)
#
# # 获取贴内图片链接
# pattern_img_src = re.compile(r'<img class="BDE_Image" src="(.*?)".*?>')
# img_src_list = pattern_img_src.findall(html_text)
# print(img_src_list)
# print(len(img_src_list))


class TiebaSpider(object):
    """
        贴吧爬虫: 爬取帖子，评论数，帖子链接，每篇贴子内的所有图片
    """

    def __init__(self):
        self.tieba = input("请输入需要爬取的贴吧名：")
        self.start_page = int(input("开始页数："))
        self.end_page = int(input("结束页数："))
        self.root_url = "http://tieba.baidu.com/"
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "zh,zh-CN;q=0.9",
            "Host": "tieba.baidu.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36",
        }

    def start_crawler(self):
        # https://tieba.baidu.com/f?kw=p站&ie=utf-8&pn=50
        for page in range(self.start_page, self.end_page + 1):
            pn = (page - 1) * 50
            next_word = {
                "kw": self.tieba,
                "ie": "utf-8",
                "pn": pn,
            }
            next_kw = parse.urlencode(next_word)
            next_url = self.root_url + "f?" + next_kw

            # 获取当前页所有帖子链接
            html_text = self.load_page(url=next_url)
            posts_link_list = self.get_current_page_all_posts(html_text)

            # 请求访问所有帖子
            for post_link in posts_link_list:
                post_html = self.load_page(post_link)
                # 请求访问帖子内的每一页
                for post_pn in range(self.get_post_page_number(post_html)):
                    # https://tieba.baidu.com/p/5547316026?pn=2
                    post_next_url = post_link + "?pn=" + str(post_pn+1)
                    html = self.load_page(post_next_url)
                    self.get_post_img(html)

    def get_current_page_all_posts(self, html):
        """
            获取当前页所有帖子的链接
        :type html: str
        :return type: list
        """
        pattern_title_link = re.compile(
            r'<a rel="noreferrer"\s+href="/(p/\d+)" title=".*?" target="_blank" class="j_th_tit ">.*?</a>')
        title_link_list = pattern_title_link.findall(html)
        print(title_link_list)
        print(len(title_link_list))
        posts_link_list = []
        for title_link in title_link_list:
            post_link = self.root_url + title_link
            posts_link_list.append(post_link)
        return posts_link_list

    def get_post_img(self, html):
        """
            获取当前帖子内的图片
        :return:
        """
        pattern_img_src = re.compile(r'<img class="BDE_Image" src="(.*?)".*?>')
        img_src_list = pattern_img_src.findall(html)
        print(img_src_list)
        print(len(img_src_list))

    def get_post_page_number(self, html):
        """
            获取帖子内回复的总页数
        :return type: int
        """
        pattern_page_number = re.compile(r'<a href="/p/.*?\?pn=(.*?)">尾页</a>')
        page_number = pattern_page_number.findall(html)
        if page_number == []:
            page_number = 1
        else:
            page_number = int(page_number[0])
        print(page_number)
        return page_number

    def get_total_page_number(self, html):
        """
            获得该贴吧总页数
        :return:
        """
        pattern_total_page_number = re.compile(
            r'<a href="//tieba.baidu.com/f\?kw=.*&pn=(\d*?)" class="last pagination-item " >尾页</a>')
        total_page_number = pattern_total_page_number.findall(html)
        if total_page_number == []:
            total_page_number = 1
        else:
            total_page_number = int(total_page_number[0])

        print(total_page_number)
        return total_page_number

    def load_page(self, url):
        # 加载页面，获取网页源码
        req = request.Request(url, headers=self.headers)
        response = request.urlopen(req)
        html_text = response.read().decode('utf-8')
        print(html_text)
        return html_text

    def get_post_info(self, html_text):
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

if __name__ == "__main__":
    tieba = TiebaSpider()
    tieba.start_crawler()
