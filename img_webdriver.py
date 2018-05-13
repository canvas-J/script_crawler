# -*- encoding=utf-8 -*-
from selenium import webdriver
import requests
from bs4 import BeautifulSoup

path='/home/gang/Myproject/coding_crawl/img/jiandan'
urls = ["http://jandan.net/ooxx/page-{}#comments".format(str(i)) for i in range(60,10,-1)]
img_url=[]
options = webdriver.ChromeOptions()
options.binary_location = '/usr/bin/chromium-browser'
# options.add_argument('window-size=1200*600')
options.add_argument('--disable-gpu')  
driver = webdriver.Chrome(chrome_options=options)
driver.set_window_size('600','600')
# driver.maximize_window()

for url in urls:
    driver.get(url)
    data = driver.page_source
    soup = BeautifulSoup(data, "lxml")
    images = soup.select("a.view_img_link")

    for i in images:               
        z=i.get('href')
        if str('gif') in str(z):
           pass
        else:
            http_url = "http:" + z
            img_url.append(http_url)
            #print("http:%s" % z)
    for j in img_url:
        r=requests.get(j)
        print('正在下载 %s......' % j)
        with open(path+j[-15:],'wb')as jpg:
            jpg.write(r.content)