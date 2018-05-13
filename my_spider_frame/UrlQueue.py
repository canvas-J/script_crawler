# -*- encoding:utf-8 -*-

class UrlQueue(object):
    def __init__(self):
        self.new_urls = set()   # 未爬取URL集合
        self.old_urls = set()   # 已爬取URL集合

    # 判断是否有未爬取的URL
    def has_new_url(self):
        return self.new_url_size()!=0

    # 获取一个未爬取的URL
    def get_new_url(self):
        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url

    # 将新的URL添加到未爬取的URL集合中
    def add_new_url(self,url):
        if url is None:
            return
        # 首先url列表不能重复，其次爬取过的过滤掉
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)

    # 将新的URLS添加到未爬取的URL集合中
    def add_new_urls(self,urls):
        if urls is None or len(urls)==0:
            return
        for url in urls:
            self.add_new_url(url)

    # 获取未爬取URL集合的s大小
    def new_url_size(self):
        return len(self.new_urls)

    # 获取已经爬取URL集合的大小
    def old_url_size(self):
        return len(self.old_urls)