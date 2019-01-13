# -*- coding:utf-8 -*-
import urllib.request, urllib.parse, http.cookiejar
import os, time, re, json, datetime
# import http.cookies, socket
from bs4 import BeautifulSoup
import pandas as pd
import requests, pickle


def getHtml(url, host='rate.taobao.com', daili='', postdata={}):
    filename = 'cookie.txt'
    # 声明一个MozillaCookieJar对象实例保存在文件中
    cj = http.cookiejar.MozillaCookieJar(filename)
    # cj =http.cookiejar.LWPCookieJar(filename)
    # ignore_discard的意思是即使cookies将被丢弃也将它保存下来
    # ignore_expires的意思是如果在该文件中 cookies已经存在，则覆盖原文件写
    if os.path.exists(filename):
        cj.load(filename, ignore_discard=True, ignore_expires=True)
    if os.path.exists('subcookie.txt'):
        cookie = open('subcookie.txt', 'r').read()
    else:
        cookie = 'ddd'
    proxy_support = urllib.request.ProxyHandler({'http': 'http://' + daili}) # 建造带有COOKIE处理器的打开专家
    if daili: # 开启代理支持
        print('current ip:' + daili)
        opener = urllib.request.build_opener(proxy_support, urllib.request.HTTPCookieProcessor(cj), urllib.request.HTTPHandler)               
    else:
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    opener.addheaders = [('User-Agent',
                          'Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5'),
                         ('Host', host),('Cookie', cookie)]
    urllib.request.install_opener(opener)
    if postdata: # 有数据需要POST
        postdata = urllib.parse.urlencode(postdata) # 数据URL编码
        html_bytes = urllib.request.urlopen(url, postdata.encode(), timeout=8).read()
    else:
        html_bytes = urllib.request.urlopen(url, timeout=8).read()
    cj.save(ignore_discard=True, ignore_expires=True) # 保存COOKIE到文件中
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

def taobao(tr_comment, urlroot, title, max=200):
    """
    页数限制：200
    """
    p = 0
    while p < max:
        # 评论页数构造
        p = p + 1
        page = str(p)

        # 网址构造
        url = urlroot + page
        # print('准备抓取' + url)
        tjson = getHtml(url).decode('utf-8', 'ignore').strip()
        pattern = re.compile(r'[(](.*)[)]', re.S)
        json_data = re.findall(pattern, tjson)[0]
        tjson = json.loads(json_data)

        # 评论
        comments = tjson['comments']
        # 评论为空，跳出
        if comments:
            pass
        else:
            break
        # 逐条评论解析
        for c in comments:
            comment = c['content']  # 初次评论内容
            date = c['date']  # 评论时间
            # print(comment,date)
            userlist = c["user"]  # 用户信息表
            user = userlist['nick']  # 用户昵称
            usergrade = userlist['displayRatePic']  # 用户等级
            appendc = c['appendList']  # 追加评论列表
            # 列表不为空
            if appendc:
                acomment = appendc[0]['content']  # 追评内容
                aday = appendc[0]['dayAfterConfirm']  # 几天后追评
            else:
                acomment = ''
                aday = ''
            replay = c['reply']  # 商家回复
            # 如果有回复
            if replay:
                replay = replay['content']
            else:
                replay = ''
            tr_comment.append(['淘宝', title, p, user, usergrade, comment, date, acomment, aday, replay])
        # print('-'*20)
        print('成功抓取{}'.format(url[-7:]))
    return tr_comment


def tmall(tr_comment, urlroot, title, max=99):
    """
    页数限制：99
    """
    p = 0
    while p < max:
        p = p + 1  # 评论页数构造
        page = str(p)
        # 网址构造
        url = urlroot + page
        # 开始抓取
        # daili = requests.get("http://192.168.43.37:5010/get/").text
        daili = ''
        # print('current ip:' + daili)
        tjson = getHtml(url, daili=daili).decode('utf-8', 'ignore').strip()
        pattern = re.compile(r'[(](.*)[)]', re.S)
        json_data = re.findall(pattern, tjson)[0]
        tjson = json.loads(json_data)

        # 失败证明没有评论
        try:
            tmallc = tjson['rateDetail']['rateList']
        except:
            return tr_comment
 
        for tc in tmallc:
            tdate = tc['rateDate'] # 评论时间
            tc1 = tc['rateContent'] # 初次评论
            tname = tc['displayUserNick'] # 评论用户
            tgrade = tc['displayRatePic'] # 用户级别
            tappendc = tc['appendComment'] # 追加评论
            if tappendc:
                tc2 = tappendc['content'] # 追评内容
                tappenddate = tappendc['days'] # 几天后追评
            else:
                tc2 = ''
                tappenddate = ''
            
            tmallb = tc['reply'] # 商家回复
            tr_comment.append(['天猫', title, p, tname, tgrade, tc1, tdate, tc2, tappenddate, tmallb])
        # print(p,tname,tgrade,tc1,tdate,tc2,tappenddate,tmallb)
        print('成功抓取{}'.format(url[-7:]))
    return tr_comment

def jd(tr_comment, urlroot, title, max=99):
    """
    页数限制：99
    """
    p = 0
    while p < max:
        p = p + 1  # 评论页数构造
        page = str(p)
        # 网址构造
        url = urlroot + page
        # 开始抓取
        # print('准备抓取' + url)
        tjson = getHtml(url).decode('utf-8', 'ignore').strip()
        pattern = re.compile(r'[(](.*)[)]', re.S)
        json_data = re.findall(pattern, tjson)[0]
        tjson = json.loads(json_data)

        # 失败证明没有评论
        try:
            tmallc = tjson["comments"]
        except:
            return tr_comment
 
        for tc in tmallc:
            tdate = tc["creationTime"] # 评论时间
            tc1 = tc["content"] # 初次评论
            tname = tc["nickname"] # 评论用户
            tgrade = tc['userLevelId'] # 用户级别
            tc2 = ''
            tappenddate = ''
            tmallb = "" # 商家回复
            tr_comment.append(['京东', title, p, tname, tgrade, tc1, tdate, tc2, tappenddate, tmallb])
        # print(p,tname,tgrade,tc1,tdate,tc2,tappenddate,tmallb)
        print('成功抓取{}'.format(url[-7:]))
    return tr_comment

def main():
    temp = pd.read_excel('../评论链接.xlsx', sheet_name='评论', encoding='GB18030')
    print('共有{}个产品链接'.format(len(temp)))

    today = time.strftime('%Y%m%d', time.localtime())
    path = '../' + today
    createjia(path)
    todays = time.strftime('%Y%m%d%H%M%S', time.localtime())
    if os.path.exists("queue.pkl"):
        queue = pickle.load(open("queue.pkl", "rb"))
        print(queue)
    else:
        queue = set()
    writer = pd.ExcelWriter('../{}/{}.xlsx'.format(today, todays))
    for num in range(len(temp)):
        if num not in queue:
            queue.add(num)
            title, t_id, userid = temp.iloc[num,[0,2,3]]
            # title, productid = temp.iloc[num,[0,1]]
            title = validateTitle(title)
            # print(title, the_url, t_id, userid)
            # urlroot = "https://rate.taobao.com/feedRateList.htm?auctionNumId={}&userNumId={}&showContent=1&currentPageNum=".format(t_id,userid)
            urlroot = "https://rate.tmall.com/list_detail_rate.htm?itemId={}&sellerId={}&content=1&order=1&currentPage=".format(t_id,userid)
            # urlroot = "https://club.jd.com/comment/skuProductPageComments.action?callback=fetchJSON_comment98vv7796&productId={}&score=0&sortType=6&pageSize=10&isShadowSku=0&rid=0&fold=1&page=".format(productid)
            # comment = taobao([], urlroot, title, 200)
            try:
                comment = tmall([], urlroot, title, 99)
                # comment = jd([], urlroot, title, 99)
                df = pd.DataFrame(comment, columns = ['类型', '商品标题', '页码', '用户昵称', '用户等级', '评论', '评论时间', '追评', '几天后追评', '商家回复'])
                # df.columns = columns
                df.to_excel(writer, sheet_name=str(num+1), index=False)
            except:
                queue.remove(num)
                pickle.dump(queue, open("queue.pkl","wb"))
    writer.save()


if __name__ == '__main__':
    a = time.clock()
    main()
    b = time.clock()
    print('运行时间：' + timetochina(b - a))