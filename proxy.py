# -*- coding: utf-8 -*-
import re, time, datetime, requests
from fake_useragent import UserAgent

proxy_ip = "http://www.xicidaili.com/nt/"
num = 1         # 爬取代理页数
headers = {'User-Agent': UserAgent().random,
   'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
   'Accept-Encoding': 'gzip'
    }

def ip_test(ip, url_for_test='https://www.baidu.com', set_timeout=2):
    try:
        r = requests.get(url_for_test, headers=headers, proxies={'http': ip[0]+':'+ip[1]}, timeout=3)
        if r.status_code == 200:
            return True
        else:
            return False
    except:
        return False

def scrawl_ip(url, num, url_for_test='https://www.baidu.com'):
    global ip_list
    ip_list = []
    start = time.time()

    for num_page in range(1, num+1):
        url = url + str(num_page)
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        content = response.text
        pattern = re.compile('<td class="country">.*?alt="Cn" />.*?</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>', re.S)
        items = re.findall(pattern, content)
        for ip in items:
            if ip_test(ip[1], url_for_test):  # 测试爬取到ip是否可用，测试通过则加入ip_list列表之中
                # print('测试通过，IP地址:' + str(ip[0]) + ':' + str(ip[1]))
                ip_list.append(ip[0]+':'+ip[1]+'\n')
        end = time.time()
        print('代理获取并测试完毕，共{}个,花费{}秒！'.format(len(ip_list),end-start))
        time.sleep(3)  # 等待3秒爬取下一页
    return ip_list

if __name__ == "__main__":
    scrawl_ip(proxy_ip, num)
    time_now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    with open("{}.txt".format(time_now),"wt") as out_file:
        for i in range(len(ip_list)):
            out_file.writelines(ip_list[i])
    print("代理暂存作名为{}.txt文件".format(time_now))