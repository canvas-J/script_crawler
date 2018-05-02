# -*- coding:utf-8 -*-
import requests
import re
import time

class QSBK:

    def __init__(self):
        self.pageIndex = 1        
        self.stories = []
        self.enable = False

    def getPage(self):
        headers = { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' }
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(self.pageIndex) + '/'
            r = requests.get(url,headers = headers)
            pageCode = r.content.decode('utf-8')
            return pageCode
        except:
            print(u"连接糗事百科失败,错误原因")
            return None
 
    #传入某一页代码，返回本页不带图片的段子列表
    def getPageItems(self):
        pageCode = self.getPage()
        if not pageCode:
            print("页面加载失败....")
            return None
        pattern = re.compile('<div.*?author clearfix.*?alt="(.*?)">.*?<div class="content.*?span>(.*?)</span>.*?<!--.*?-->.*?<div class="(.*?)?">.*?<span class="stats-vote.*?number">(.*?)</i>.*?<span class="stats-comments.*?number">(.*?)</i>',re.S)
        # 0、笑话作者
        # 1、笑话内容
        # 2、带图片属性
        # 3、点赞数
        # 4、评论数

        items = re.findall(pattern,pageCode)
        #用来存储每页的段子们
        pageStories = []
        #遍历正则表达式匹配的信息
        for item in items:
            #如果不含有图片，把它加入list中
            if item[2] != "thumb":
                replaceBR = re.compile('<br/>')
                text = re.sub(replaceBR,"\n",item[1])
                #item[0]是一个段子的发布者，item[1]是内容，item[3]是点赞数,item[4]是评论数
                pageStories.append([item[0].strip(),text.strip(),item[3].strip(),item[4].strip()])
        return pageStories
 
    #加载并提取页面的内容，加入到列表中
    def loadPage(self):
        #如果当前未看的页数少于2页，则加载新一页
        if self.enable == True:
            if len(self.stories) < 2:
                #获取新一页
                pageStories = self.getPageItems()
                #将该页的段子存放到全局list中
                if pageStories:
                    self.stories.append(pageStories)
                    #获取完之后页码索引加一，表示下次读取下一页
                    self.pageIndex += 1
    
    #调用该方法，每次敲回车打印输出一个段子
    def getOneStory(self,pageStories,nowpage):
        #遍历一页的段子
        for one in pageStories:
            #等待用户输入
            i = input()
            #每当输入回车一次，判断一下是否要加载新页面
            self.loadPage()
            #如果输入Q则程序结束
            if input == "Q":
                self.enable = False
                return
            print("第{}页\t发布人:{}\t赞:{}\t评论：{}\n{}".format(nowpage,one[0],one[2],one[3],one[1]))
    
    #开始方法
    def start(self):
        print(u"正在读取糗事百科,按回车查看新段子，Q退出")
        #使变量为True，程序可以正常运行
        self.enable = True
        #先加载一页内容
        self.loadPage()
        #局部变量，控制当前读到了第几页
        nowPage = 0
        while self.enable:
            if len(self.stories) > 0:
                #从全局list中获取一页的段子
                pageStories = self.stories[0]
                #当前读到的页数加一
                nowPage += 1
                #将全局list中第一个元素删除，因为已经取出
                del self.stories[0]
                #输出该页的段子
                self.getOneStory(pageStories,nowPage)
 
spider = QSBK()
spider.start()



'''
import requests
import re

pageIndex = 1
storyPages = []

headers = { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' }
url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex) + '/'
r = requests.get(url,headers = headers)
pageCode = r.content.decode('utf-8')

pattern = re.compile('<div.*?author clearfix.*?alt="(.*?)">.*?<div class="content.*?span>(.*?)</span>.*?<!--.*?-->.*?<div class="(.*?)?">.*?<span class="stats-vote.*?number">(.*?)</i>.*?<span class="stats-comments.*?number">(.*?)</i>',re.S)
        # 0、笑话作者
        # 1、笑话内容
        # 2、带图片属性
        # 3、点赞数
        # 4、评论数
items = re.findall(pattern,pageCode)
stories = []
for item in items:
    #如果不含有图片，把它加入list中
    if item[2] != "thumb":
        replaceBR = re.compile('<br/>')
        text = re.sub(replaceBR,"\n",item[1])
        #item[0]是一个段子的发布者，item[1]是内容，item[3]是点赞数,item[4]是评论数
        stories.append([item[0].strip(),text.strip(),item[3].strip(),item[4].strip()])

while 1:
    if len(storyPages) < 2:
        #获取新一页
        storyPages.append(stories)
        #获取完之后页码索引加一，表示下次读取下一页
        pageIndex += 1

    for i in storyPages[0]:
        o = input()
        print("第{}页\t发布人:{}\t赞:{}\t评论：{}\n{}".format(pageIndex-1,i[0],i[2],i[3],i[1]))
    del storyPages[0]
'''

