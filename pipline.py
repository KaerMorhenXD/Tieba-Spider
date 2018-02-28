import os

from TiebaCrawler_v2.proxy import get_response
from TiebaCrawler_v2.config import IMG_HEADERS

def save_img(url, tieba):
    """
        保存图片到本地
    :param url: 图片地址 str
    :param tieba: 爬取的贴吧名 str
    :return:
    """
    print("---- 正在保存图片 %s 到当前目录文件夹 tieba_image/%s ..." % (url, tieba))
    file_path = os.getcwd() + "/tieba_image/" + tieba
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    with open('./tieba_image/' + tieba + "/" + url[-17:], 'wb') as f:
        img = get_response(url, headers=IMG_HEADERS, timeout=7).content
        f.write(img)
