import queue
import threading
import time
import random

from TiebaCrawler_v2.crawler import Crawler
from TiebaCrawler_v2.pipline import save_img


class PostThread(threading.Thread):
    """
        从 tieba_queue 队列取贴吧每一页的 url，
        调用 crawler 的 post_url 方法，将返回的该页下的所有帖子的 url 放进 post_queue
    """

    # def __init__(self):
    #     super(PostThread, self).__init__(self)

    def run(self):
        while not tieba_queue.empty():
            print("PostThread...")
            ever_page_url = tieba_queue.get()
            print("正在访问的url：" + ever_page_url)
            post_url_list = crawler.post_url(ever_page_url)
            for url in post_url_list:
                post_queue.put(url)

            time.sleep(random.uniform(0.8, 1.5))


class PostPageThread(threading.Thread):
    """
        贴子内每一页的线程
    """

    def run(self):
        while not EXIT_POST_QUEUE:
            print("Post_Page_Thread...")
            post_url = post_queue.get()
            post_page_url_list = crawler.post_page_url(post_url)
            # 将帖子所有页的 url 添加到队列
            for url in post_page_url_list:
                post_page_queue.put(url)

            time.sleep(random.uniform(0.8, 1.5))


class ImageThread(threading.Thread):
    """
        图片处理线程
    """

    def __init__(self):
        super(ImageThread, self).__init__()

    def run(self):
        while not EXIT_POST_PAGE:
            print("ImageThread...")
            post_url = post_page_queue.get()
            img_url_list = crawler.img_url(post_url)
            if img_url_list:
                for url in img_url_list:
                    img_queue.put(url)
            else:
                print("这页帖子好像没有图片( •̀ ω •́ )")

            time.sleep(random.uniform(0.8, 1.5))

class SaveThread(threading.Thread):
    """
        保存线程
    """
    def __init__(self, t_lock):
        super(SaveThread, self).__init__()
        self.lock = t_lock

    def run(self):
        while not EXIT_IMG_QUEUE:
            img_src = img_queue.get()
            # 调用 pipline.py 处理文件
            with self.lock:
                save_img(img_src, tieba)

            time.sleep(random.uniform(1, 2))

# 线程数
THREAD_NUMBER = 2

# 退出标志
EXIT_POST_QUEUE = False
EXIT_POST_PAGE = False
EXIT_IMG_QUEUE = False

# 创建锁
lock = threading.Lock()

if __name__ == "__main__":
    tieba_queue = queue.Queue()
    post_queue = queue.Queue()
    post_page_queue = queue.Queue()
    img_queue = queue.Queue()

    tieba = input("请输入贴吧名：")
    start_page = int(input("请输入起始页："))
    end_page = int(input("请输入终止页："))

    # 填充第一次要爬取的页的 url 到队列
    crawler = Crawler(tieba, start_page, end_page, post_queue, img_queue)
    for start_url in crawler.tieba_next_page():
        tieba_queue.put(start_url)

    # 总帖子处理线程
    post_threads = []
    for i in range(THREAD_NUMBER if end_page + 1 - start_page > THREAD_NUMBER else end_page - start_page):
        thread = PostThread()
        thread.start()
        post_threads.append(thread)

    # 帖子每一页处理线程
    post_page_threads = []
    for i in range(THREAD_NUMBER):
        thread = PostPageThread()
        thread.start()
        post_page_threads.append(thread)

    # 图片处理线程
    image_threads = []
    for i in range(THREAD_NUMBER):
        thread = ImageThread()
        thread.start()
        post_threads.append(thread)

    save_threads = []
    for i in range(THREAD_NUMBER):
        thread = SaveThread(lock)
        thread.start()
        save_threads.append(thread)

    for t in post_threads:
        t.join()
    print("退出 Post_Thread ...")

    # 等待帖子每一页队列空
    while not post_queue.empty():
        pass
    EXIT_POST_QUEUE = True

    for t in post_page_threads:
        t.join()
    print("结束 Post_Page_Thread ...")

    # 等待帖子每一页队列空
    while not post_page_queue.empty():
        pass
    EXIT_POST_PAGE = True

    for t in image_threads:
        t.join()
    print("结束 Image_Thread ...")

    # 等待图片队列空
    while not img_queue.empty():
        pass
    EXIT_IMG_QUEUE = True

    for t in save_threads:
        t.join()
    print("结束 Save_Thread ...")


