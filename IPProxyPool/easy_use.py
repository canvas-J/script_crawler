# -*- encoding:utf-8 -*-
import requests, json
import random

useragent_list = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6"
    ]
headers = {'User-Agent': random.choice(useragent_list),
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    'Accept-Encoding': 'gzip'
    }


# 获取5个代理，随机挑选一个使用
response = requests.get('http://127.0.0.1:8000/?count=5')
# response = requests.get('http://127.0.0.1:8000/?types=0&count=5&country=中国')
json_dict = json.loads(response.text)
ip = json_dict[int(random.choice('01234'))]
proxies = {
    'http':'http://{}:{}'.format(ip[0],ip[1]),
    'https':'http://{}:{}'.format(ip[0],ip[1])
    }
print(proxies)


# 确认测试
# def ip_test(proxies):
#     try:
#         r = requests.get('http://ip.chinaz.com', headers=headers, proxies=proxies, timeout=3)
#         if r.status_code == 200:
#             print("it's fine")
#         else:
#             print("访问失败")
#     except:
#         print("超时？")

# ip_test(proxies)