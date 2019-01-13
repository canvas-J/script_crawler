# -*- coding:utf-8 -*-
import urllib.request, urllib.parse, http.cookiejar
import os, time, re, json, datetime
from bs4 import BeautifulSoup
import pandas as pd
import requests, pickle
from fake_useragent import UserAgent


def getHtml(url, host='jd.com', daili='', postdata={}):
    cj = http.cookiejar.MozillaCookieJar()
    proxy_support = urllib.request.ProxyHandler({'http': 'http://' + daili})
    if daili:
        print('current ip:' + daili)
        opener = urllib.request.build_opener(proxy_support, urllib.request.HTTPCookieProcessor(cj), urllib.request.HTTPHandler)
    else:
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    opener.addheaders = [('User-Agent', UserAgent().random),('Host', host)]
    urllib.request.install_opener(opener)
    html_bytes = urllib.request.urlopen(url, timeout=8).read()
    # print(html_bytes).decode('GB18030', 'ignore').strip()
    return html_bytes

# 去除标题中的非法字符 (Windows)
def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/\:*?"<>|'
    new_title = re.sub(rstr, "", title)
    return new_title

def createjia(path):
    try:
        os.makedirs(path)
    except:
        print('目录已经存在：' + path)


def timetochina(longtime, formats='{}天{}小时{}分钟{}秒'):
    day = 0
    hour = 0
    minutue = 0
    second = 0
    try:
        if longtime > 60:
            second = longtime % 60
            minutue = longtime // 60
        else:
            second = longtime
        if minutue > 60:
            hour = minutue // 60
            minutue = minutue % 60
        if hour > 24:
            day = hour // 24
            hour = hour % 24
        return formats.format(day, hour, minutue, second)
    except:
        pass

def jd(tr_comment, urlroot, title, max=99):
    """
    页数限制：99
    """
    p = 0
    while p < max:
        p = p + 1
        page = str(p)
        url = urlroot + page
        # daili = requests.get("http://192.168.1.110:5010/get/").text
        # print('current ip:' + daili)
        try:
            tjson = getHtml(url).decode('GB18030', 'ignore').strip()
            pattern = re.compile(r'[(](.*)[)]', re.S)
            json_data = re.findall(pattern, tjson)[0]
            tjson = json.loads(json_data)
            tmallc = tjson["comments"]
            for tc in tmallc:
                tdate = tc["creationTime"] # 评论时间
                tc1 = tc["content"] # 初次评论
                tname = tc["nickname"] # 评论用户
                tgrade = tc['userLevelId'] # 用户级别
                tc2 = ''
                tappenddate = ''
                tmallb = "" # 商家回复
                tr_comment.append(['京东', title, p, tname, tgrade, tc1, tdate, tc2, tappenddate, tmallb])
            print('成功抓取{}'.format(url[-7:]))
        except:
            return tr_comment
        print(p,tname,tgrade,tc1,tdate,tc2,tappenddate,tmallb)
    return tr_comment

def main():
    temp = pd.read_excel('../评论链接.xlsx', sheet_name='京东', encoding='GB18030')
    print('共有{}个产品链接'.format(len(temp)))
    today = time.strftime('%Y%m%d', time.localtime())
    path = '../' + today
    createjia(path)
    todays = time.strftime('%Y%m%d%H%M%S', time.localtime())
    writer = pd.ExcelWriter('../{}/{}.xlsx'.format(today,todays))
    for num in range(len(temp)):
        title, productid = temp.iloc[num,[0,1]]
        print(title, productid)
        title = validateTitle(title)
        urlroot = "https://club.jd.com/comment/skuProductPageComments.action?callback=fetchJSON_comment98vv86&productId={}&score=0&sortType=6&pageSize=10&isShadowSku=0&rid=0&fold=1&page=".format(productid)
        comment = jd([], urlroot, title, 99)
        df = pd.DataFrame(comment, columns = ['类型', '商品标题', '页码', '用户昵称', '用户等级', '评论', '评论时间', '追评', '几天后追评', '商家回复'])
        df.to_excel(writer, sheet_name=str(num+1), index=False)
        print('Done')
    writer.save()


if __name__ == '__main__':
    a = time.clock()
    main()
    b = time.clock()
    print('运行时间：' + timetochina(b - a))