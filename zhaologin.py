# -*- coding: utf-8 -*-
import requests
import http.cookiejar as cookielib
import re
import time
import os.path
from PIL import Image, ImageEnhance
import pytesser3



# 构造 Request headers
agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'
headers = {
    "Host": "www.chinabidding.cn",
    "Referer": "https://www.chinabidding.cn/cblcn/member.login/login",
    'User-Agent': agent
}

# 使用登录cookie信息
session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookies')
try:
    session.cookies.load(ignore_discard=True)
except:
    print("Cookie 未能加载")


def get_id():
    '''动态变化的参数,指向验证码和登录'''
    index_url = 'https://www.chinabidding.cn/cblcn/member.login/login'
    # 获取登录时需要用到的randomID
    index_page = session.get(index_url, headers=headers)
    html = index_page.text
    pattern = r'login/captcha\?randomID=(.*?)"'
    # 这里的_xsrf 返回的是一个list
    randomID = re.findall(pattern, html)
    return randomID[0]


# 获取验证码
def get_captcha(randomID):
    captcha_url = 'https://www.chinabidding.cn/cblcn/member.login/captcha?randomID={}'.format(randomID)
    r = session.get(captcha_url, headers=headers)
    with open('captcha.jpg', 'wb') as f:
        f.write(r.content)
        f.close()
    # im = Image.open('captcha.jpg')
    # img = ImageEnhance.Contrast(im).enhance(2)
    # captcha = pytesser3.image_to_string(img)
    # print(captcha)
    captcha = input('请手动打开图片，并输入验证码')
    return captcha


def isLogin():
    # 通过查看用户个人信息来判断是否已经登录
    url = "https://www.chinabidding.cn/cblcn/busiroom/home"
    # url = 'http://192.168.99.100:8050/render.html?url='+url
    login_code = session.get(url, headers=headers, allow_redirects=False).status_code
    if login_code == 200:
        return True
    else:
        return False
    # check = session.get(url, headers=headers, allow_redirects=False)
    # print(check.text)


def login(secret, account):
    randomID = get_id()
    headers["X-Requested-With"] = "XMLHttpRequest"
    postdata = {
        'name': account,
        'password': secret,
        'url': '',
        'yzm': '',
        'randomID': randomID,
        't':'1547132532835',
        }
    postdata["yzm"] = get_captcha(randomID)
    post_url = 'https://www.chinabidding.cn/cblcn/member.login/logincheck'
    login_page = session.post(post_url, data=postdata, headers=headers)
    # login_code = login_page.json()
    # print(login_code['msg'])
    # 保存 cookies 到文件，
    session.cookies.save()


if __name__ == '__main__':
    if isLogin():
        print('您已经登录')
    else:
        account = '名'
        secret = '密'
        login(secret, account)
