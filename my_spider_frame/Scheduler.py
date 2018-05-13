#coding:utf-8
from UrlQueue import UrlQueue
from HtmlDownloader import HtmlDownloader
from HtmlParser import HtmlParser
from DataOutput import DataOutput


class Spider_Scheduler(object):
    def __init__(self):
        self.urlmanager = UrlQueue()
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        self.output = DataOutput()

    def crawl(self,root_url):
        # 入口放url种子
        self.urlmanager.add_new_url(root_url)
        # 判断url管理器中是否有新的url，同时判断抓取了多少个url
        while(self.urlmanager.has_new_url() and self.urlmanager.old_url_size()<100):
            try:
                # 从URL管理器获取新的url
                new_url = self.urlmanager.get_new_url()
                # HTML下载器下载网页
                html = self.downloader.download(new_url)
                # HTML解析器抽取网页数据
                new_urls, data = self.parser.parser(new_url,html)
                # 将抽取到url添加到URL管理器中
                self.urlmanager.add_new_urls(new_urls)
                # 存储器将数据序列化
                self.output.data_to_list(data)
                print("已经抓取%s个链接"%self.urlmanager.old_url_size())
            except Exception as e:
                print("crawl failed")
        # 存储器输出成指定格式
        self.output.output_html()

if __name__ == "__main__":
    frame = SpiderScheduler()
    frame.crawl("http://baike.baidu.com/view/284853.htm")
