# -*- coding: utf-8 -*- 
import os
import sys
import requests
from tkinter import *

"""解码百度图片搜索json中传递的url
抓包可以获取加载更多图片时，服务器向网址传输的json。
其中originURL是特殊的字符串
解码前：
ippr_z2C$qAzdH3FAzdH3Ffl_z&e3Bftgwt42_z&e3BvgAzdH3F4omlaAzdH3Faa8W3ZyEpymRmx3Y1p7bb&mla
解码后：
http://s9.sinaimg.cn/mw690/001WjZyEty6R6xjYdtu88&690
使用下面两张映射表进行解码。
"""
str_table = {
    '_z2C$q': ':',
    '_z&e3B': '.',
    'AzdH3F': '/'
}

char_table = {
    'w': 'a',
    'k': 'b',
    'v': 'c',
    '1': 'd',
    'j': 'e',
    'u': 'f',
    '2': 'g',
    'i': 'h',
    't': 'i',
    '3': 'j',
    'h': 'k',
    's': 'l',
    '4': 'm',
    'g': 'n',
    '5': 'o',
    'r': 'p',
    'q': 'q',
    '6': 'r',
    'f': 's',
    'p': 't',
    '7': 'u',
    'e': 'v',
    'o': 'w',
    '8': '1',
    'd': '2',
    'n': '3',
    '9': '4',
    'c': '5',
    'm': '6',
    '0': '7',
    'b': '8',
    'l': '9',
    'a': '0'
}
# str 的translate方法需要用单个字符的十进制unicode编码作为key
# value 中的数字会被当成十进制unicode编码转换成字符
# 也可以直接用字符串作为value
char_table = {ord(key): ord(value) for key, value in char_table.items()}
headers = {
    'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',\
    'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11',\
    'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'
}

def decode_info(url):
    # 先替换字符串
    for key, value in str_table.items():
        url = url.replace(key, value)
    # 再替换剩下的字符
    return url.translate(char_table)

def getManyPages(keyword, pages):
    params=[]
    for i in range(30, 30*int(pages)+30, 30):
        params.append({
                      'tn': 'resultjson_com',
                      'ipn': 'rj',
                      'ct': 201326592,
                      'is': '',
                      'fp': 'result',
                      'queryWord': keyword,
                      'cl': 2,
                      'lm': -1,
                      'ie': 'utf-8',
                      'oe': 'utf-8',
                      'adpicid': '',
                      'st': -1,
                      'z': '',
                      'ic': 0,
                      'word': keyword,
                      's': '',
                      'se': '',
                      'tab': '',
                      'width': '',
                      'height': '',
                      'face': 0,
                      'istype': 2,
                      'qc': '',
                      'nc': 1,
                      'fr': '',
                      'pn': i,
                      'rn': 30,
                      'gsm': '1e',
                      '1488942260214': ''
                  })
    url = 'https://image.baidu.com/search/acjson'
    urls = []
    for i in params:
        urls.append(requests.get(url, params=i, headers=headers).json().get('data'))
    return urls

def getImg(localPath, count):
    try:
        image_url = decode_info(url_info)
        print('正在下载：%s' % image_url)
        im = requests.get(image_url, headers=headers, timeout=5)
        open(localPath + '/%d.jpg' % count, 'wb').write(im.content)
    except Exception as e:
        print("抛出异常：", image_url)
        print(e)
        return False

def main():
    keyword = var1.get()
    page_num = var2.get()
    dataList = getManyPages(keyword, page_num)  # 参数1:关键字，参数2:要下载的页数
    dirpath = os.path.join(sys.path[0], 'results')  # 保存到同级目录下的results文件夹内
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)

    global url_info, count
    count = 1
    for url in dataList:
        for info in url:
            url_info = info.get('objURL')
            if url_info != None:
                getImg(dirpath, count) # 参数2:指定保存的路径
                count += 1
            else:
                print('图片链接不存在')
    root.destroy()


#声名一个tk（你可以把tk理解为一个窗口）
root = Tk()
#这里填写什么，生成窗口的名字就是什么
root.title("输入获取参数")

L1 = Label(root,text = '关键词:').grid(column = 0,row = 0)
var1 = StringVar()
var1.set("风景")
E1 = Entry(root,textvariable = var1, bd = 2).grid(column = 1,row = 0)

L2 = Label(root,text = '获取页数:').grid(column = 0,row = 1)
var2 = StringVar()
var2.set("10")
E2 = Entry(root,textvariable = var2, bd = 2).grid(column = 1,row = 1)

Button1 = Button(root,text = "开始获取",command=main).grid(column = 1,row = 3)
root.mainloop()

