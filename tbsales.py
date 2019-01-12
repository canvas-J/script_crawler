import pandas as pd
import os, logging, traceback, sys
import re, datetime, requests, json
import urllib.request, urllib.parse, http.cookiejar


def getHtml(url, daili='', postdata={}):
    cj = http.cookiejar.MozillaCookieJar(filename='cookie.txt') # 获取cookie对象
    if os.path.exists('cookie.txt'):
        cj.load('cookie.txt', ignore_discard=True, ignore_expires=True)
    proxy_support = urllib.request.ProxyHandler({'http': 'http://' + daili})
    if daili:
        print('current ip:' + daili)
        opener = urllib.request.build_opener(proxy_support, urllib.request.HTTPCookieProcessor(cj), urllib.request.HTTPHandler)                                           
    else:
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj)) # 建立一个带cookie的管理器
    if os.path.exists('subcookie.txt'):
        cookie = open('subcookie.txt', 'r').read()
    else:
        cookie = 'ddd'
    opener.addheaders = [('User-Agent',
                          'Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5'),
                         ('Host', 'taobao.com'), ('Cookie', cookie)] # 添加头部和cookie       
    if postdata:
        postdata = urllib.parse.urlencode(postdata)
        html_bytes = opener.open(url, postdata.encode(), timeout=8).read()
    else:
        html_bytes = opener.open(url, timeout=8).read()
    cj.save(ignore_discard=True, ignore_expires=True)
    return html_bytes.decode('utf-8', 'ignore').strip()

def get_items(res):
    g_page = re.search(r'g_page_config = (.*?);\n', res)
    g_page_json = json.loads(g_page.group(1))
    p_items = g_page_json['mods']['itemlist']['data']['auctions']
    result = []
    for each in p_items:
        # title = re.sub(r'<(.*?)>', '', each['title'])
        raw_title = each['raw_title']
        view_price = each['view_price']
        view_sales = each['view_sales']
        comment_count = each['comment_count']
        user_id = each['user_id']
        result.append([raw_title, view_price, view_sales, comment_count, user_id])
    return result

def main():
    keyword = input("请输入商品名：")
    num = input("请输入总页数：")
    page_num = 1 if num == '' else int(num)
    data = []
    logging.basicConfig(level=logging.ERROR,  
                format='%(asctime)s %(levelname)s %(message)s',  
                datefmt='%Y-%m-%d %H:%M:%S',
                filename='tmall.log',
                filemode='w')
    url = "https://s.taobao.com/search"
    bar_length = 50
    for page in range(page_num):
        params = {'q':keyword,'sort':'sale-desc','s':str(page*44)} #字典中第二项是按销量排序
        res = getHtml(url, postdata=params)
        # print(res)
        hashes = '#' * int((page+1)/page_num * bar_length)
        spaces = ' ' * (bar_length - len(hashes))
        sys.stdout.write("\r进度: [{}] {:.0%}".format(hashes + spaces, (page+1)/page_num))
        sys.stdout.flush()
        try:
            data += get_items(res)
        except:
            logging.error('页码：'+str(page+1)+'\n'+traceback.format_exc()+'-'*60+'\n')
            break
    matrix = pd.DataFrame(data, columns=['标题', '价格', '成交量', '评论数', '卖家ID']) # 
    matrix.to_excel('{}-{}销量.xlsx'.format(datetime.datetime.now().strftime('%Y-%m-%d-%H'),keyword), encoding='GB18030', index=False)


if __name__ == "__main__":
    main()

'''
headers = {
    "Host": "taobao.com",
    'User-Agent': 'Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5'
    }
session = requests.session()
session.cookies = http.cookiejar.MozillaCookieJar(filename='cookies.txt')
try:
    session.cookies.load(ignore_discard=True)
except:
    print("Cookie 未能加载")

cookie = open('subcookie.txt', 'r').read()
cookieDict = {}
items = cookie.split(';')
for item in items:
    key = item.split('=')[0].replace(' ', '')# 记得去除空格
    value = item.split('=')[1]
    cookieDict[key] = value

def getHtml(url, postdata={}):
    # index_page = session.get(url, data=postdata, cookies=cookieDict, headers=headers)
    index_page = session.get(url, data=postdata, headers=headers)
    return index_page.text
'''