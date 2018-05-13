# -*- encoding:utf-8 -*-
import re
import urllib.parse
from bs4 import BeautifulSoup


class HtmlParser(object):
    # 解析网页，获取url和data
    def parser(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        new_urls = self._get_new_urls(page_url, soup)
        new_data = self._get_new_data(page_url, soup)
        return new_urls, new_data

    # 网址采用集合，可以去重
    def _get_new_urls(self, page_url, soup):
        new_urls = set()
        links = soup.find_all('a', href=re.compile(r'/item/.*'))
        for link in links:
            new_url = link['href']
            new_full_url = urllib.parse.urljoin(page_url, new_url)
            new_urls.add(new_full_url)
        return new_urls

    # 数据采用字典（键值对）序列化，方便输出为JSON和CSV格式
    def _get_new_data(self, page_url, soup):
        data = {}
        data['url'] = page_url
        title = soup.find('dd', class_='lemmaWgt-lemmaTitle-title').find('h1')
        data['title'] = title.get_text()
        summary = soup.find('div', class_='lemma-summary')
        # 获取到tag中包含的所有文版内容包括子孙tag中的内容,并将结果作为Unicode字符串返回
        data['summary'] = summary.get_text()
        return data
