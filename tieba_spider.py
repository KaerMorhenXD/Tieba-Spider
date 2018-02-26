import requests
import re
import time
import random
import os

USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; zh-CN)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36",
]

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "zh,zh-CN;q=0.9",
    "Host": "tieba.baidu.com",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": random.choice(USER_AGENT_LIST),
}
IMG_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "zh,zh-CN;q=0.9",
    "Cache-Control": "max-age=0",
    "Host": "imgsa.baidu.com",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": random.choice(USER_AGENT_LIST),
}


class TiebaSpider(object):
    """
        贴吧爬虫: 爬取帖子，评论数，帖子链接，每篇贴子内的所有图片
    """

    def __init__(self):
        self.root_url = "http://tieba.baidu.com/"
        self.url = "http://tieba.baidu.com/f"
        self.tieba = input("请输入需要爬取的贴吧名：")
        self.start_page = int(input("开始页数："))
        self.end_page = int(input("结束页数："))
        self.page_validaty_check()

    def page_validaty_check(self):
        """
            检查页数合法性
        :return:
        """
        if self.start_page <= 0:
            self.start_page = 1

        page_number = self.get_total_page_number()
        if self.end_page > page_number:
            self.end_page = page_number

        if self.end_page < self.start_page:
            self.start_page, self.end_page = self.end_page, self.start_page

    def get_total_page_number(self):
        """
            获得该贴吧总页数
        :return type: int
        """
        kw = {
            "ie": "utf-8",
            "kw": self.tieba,
            "fr": "search",
        }
        html = self.load_page(self.url, params=kw).text

        pattern_total_page_number = re.compile(
            r'<a href="//tieba.baidu.com/f\?kw=.*&pn=(\d*?)" class="last pagination-item " >尾页</a>')
        total_page_number = pattern_total_page_number.findall(html)
        if total_page_number == []:
            total_page_number = 1
        else:
            total_page_number = int(total_page_number[0])

        return total_page_number

    def start_crawler(self):
        """
            深度优先遍历所有帖子
        :return:
        """
        # https://tieba.baidu.com/f?kw=p站&ie=utf-8&pn=50
        for page in range(self.start_page, self.end_page + 1):
            print("正在爬取 '%s'吧 第 %d 页" % (self.tieba, page))
            pn = (page - 1) * 50
            next_kw = {
                "kw": self.tieba,
                "ie": "utf-8",
                "pn": pn,
            }
            # 获取当前页所有帖子链接
            html = self.load_page(url=self.url, params=next_kw).text
            posts_link_list, title_list = self.get_current_page_all_posts(html)

            # 请求访问所有帖子
            for post_link, title in zip(posts_link_list, title_list):
                print("-- 正在访问帖子的标题：'%s'" % title)
                post_html = self.load_page(post_link).text

                # 请求访问帖子内的每一页
                for post_pn in range(self.get_post_page_number(post_html)):
                    # https://tieba.baidu.com/p/5547316026?pn=2
                    post_next_url = post_link + "?pn=" + str(post_pn + 1)
                    print("---- 正在爬取帖子：'%s'第 %d 页" % (title, post_pn + 1))
                    post_html = self.load_page(post_next_url).text
                    self.get_post_img(post_html)
                    print("---- 休息...休息一下..._(:з)∠)_\n")
                    time.sleep(random.uniform(1, 2))

    def get_proxy(self):
        """
            获得一个代理 IP
        :return:
        """
        return requests.get("http://127.0.0.1:5010/get/").text

    def delete_proxy(self, proxy):
        """
            删除一个代理 IP
        :return:
        """
        requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

    def load_page(self, url, params=None, headers=HEADERS):
        # 使用代理 IP 加载页面，获取网页源码
        retry_count = 3
        proxy = self.get_proxy()
        while retry_count > 0:
            try:
                html = requests.get(url, params, headers=headers, proxies={"http": "http://{}".format(proxy)}, timeout=20)
                print(html.url)
                return html
            except Exception as e:
                retry_count -= 1
                print("访问网页失败，再次尝试...: " + str(e))
        # 出错3次，删除该代理 IP，并更换IP加载页面
        self.delete_proxy(proxy)
        return self.load_page(url=url, params=params, headers=headers)

    def get_current_page_all_posts(self, html):
        """
            获取当前页所有帖子的链接和标题
        :type html: str
        :return type: list
        """
        # 获得帖子标题
        pattern_title = re.compile(
            r'<a rel="noreferrer"\s+href="/p/\d+" title=".*?" target="_blank" class="j_th_tit ">(.*?)</a>')
        title_list = pattern_title.findall(html)

        # 帖子链接
        pattern_title_link = re.compile(
            r'<a rel="noreferrer"\s+href="/(p/\d+)" title=".*?" target="_blank" class="j_th_tit ">.*?</a>')
        title_link_list = pattern_title_link.findall(html)
        # print(title_link_list)

        print("当前页共有 %d 篇帖子，请耐心等待..." % len(title_link_list))
        posts_link_list = []
        for title_link in title_link_list:
            post_link = self.root_url + title_link
            posts_link_list.append(post_link)
        return posts_link_list, title_list

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
        # print(page_number)
        return page_number

    def get_post_img(self, html):
        """
            获取当前帖子内的图片并保存到本地
        :return:
        """
        pattern_img_src = re.compile(r'<img class="BDE_Image" src="(.*?)".*?>')
        img_src_list = pattern_img_src.findall(html)

        if img_src_list == []:
            print("---- 这页看起来没有图片( •̀ ω •́ )...下一页走起...")
        else:
            print(img_src_list)
            # print(len(img_src_list))
            print("---- 正在保存图片到当前目录文件夹 tieba_image/%s ..." % self.tieba)
            for img_src in img_src_list:
                file_path = os.getcwd() + "/tieba_image/" + self.tieba
                if not os.path.exists(file_path):
                    os.makedirs(file_path)
                with open('./tieba_image/' + self.tieba + "/" + img_src[-17:], 'wb') as f:
                    img = requests.get(img_src, headers=IMG_HEADERS).content
                    f.write(img)
                    time.sleep(random.uniform(1, 2))

    def get_post_info(self, html):
        # 匹配帖子标题
        pattern_title = re.compile(
            r'<a rel="noreferrer"\s+href="/p/\d+" title=".*?" target="_blank" class="j_th_tit ">(.*?)</a>')
        title_list = pattern_title.findall(html)
        print(title_list)
        print(len(title_list))

        # 匹配帖子链接
        pattern_title_link = re.compile(
            r'<a rel="noreferrer"\s+href="/(p/\d+)" title=".*?" target="_blank" class="j_th_tit ">.*?</a>')
        title_link_list = pattern_title_link.findall(html)
        print(title_link_list)
        print(len(title_link_list))

        # 匹配评论数
        pattern_comment_nums = re.compile(r'<span class="threadlist_rep_num center_text"\s*title="回复">(.*?)</span>')
        comment_nums_list = pattern_comment_nums.findall(html)
        print(comment_nums_list)
        print(len(comment_nums_list))


if __name__ == "__main__":
    tieba = TiebaSpider()
    tieba.start_crawler()
