"""
    代理 IP 池 API
"""
import requests
from TiebaCrawler_v2.config import HEADERS


def get_proxy():
    """
        获得一个代理 IP
    :return: str
    """
    return requests.get("http://127.0.0.1:5010/get/").text


def delete_proxy(proxy):
    """
        删除一个代理 IP
    :return:
    """
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))


def get_all_proxy():
    """
        获得全部可用的代理 IP
    :return: str
    """
    return requests.get("http://127.0.0.1:5010/get_all").text


def get_status():
    """
        查看可用代理 IP 数量
    :return: int
    """
    return int(requests.get("http://127.0.0.1:5010/get_status").text)


def get_response(url, params=None, headers=HEADERS, timeout=20):
    """
        使用代理 IP 接口加载页面，获取网页源码
    :param url:
    :param params:
    :param headers:
    :return: response 对象
    """
    retry_count = 3
    proxy = get_proxy()
    while retry_count > 0:
        try:
            response = requests.get(url, params, headers=headers, proxies={"http": "http://{}".format(proxy)},
                                    timeout=timeout)
            print("请求：" + response.url)
            return response
        except Exception as e:
            retry_count -= 1
            print("访问网页失败，再次尝试...: " + str(e))
    # 出错3次，删除该代理 IP，并更换 IP 加载页面
    delete_proxy(proxy)
    return get_response(url=url, params=params, headers=headers, timeout=timeout)
