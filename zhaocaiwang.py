# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()
import pickle, re, requests, os, json
import time
# from openpyxl import Workbook
from random import random
from lxml import etree
from gevent.pool import Group
# from config import *
import http.cookiejar as cookielib
# import pandas as pd



class Login(object):
    """招采网登录"""
    def __init__(self, user='名',password='密'):
        self.headers = {"Host": "www.chinabidding.cn",
                "Referer": "https://www.chinabidding.cn/cblcn/member.login/login",
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
                }
        self.user = user
        self.passwd = password
        self.url = 'http://projects.rccchina.com/user'
        self.session = requests.session()

    def get_captcha(self, randomID):
        captcha_url = 'https://www.chinabidding.cn/cblcn/member.login/captcha?randomID={}'.format(randomID)
        r = self.session.get(captcha_url, headers=self.headers)
        with open('captcha.jpg', 'wb') as f:
            f.write(r.content)
            f.close()
        # im = Image.open('captcha.jpg')
        # img = ImageEnhance.Contrast(im).enhance(2)
        # captcha = pytesser3.image_to_string(img)
        # print(captcha)
        captcha = input('请手动打开图片，并输入验证码')
        return captcha

    @property
    def logined(self):
        return self._Session

    @logined.setter
    def logined(self):
        #生成登陆的Session对象
        print('aaaa')
        if os.path.exists('Session'):
            with open('Session', 'rb') as f:
                self.session = pickle.load(f)
            #加一个有效验证吧
            welcome = 'https://www.chinabidding.cn/cblcn/busiroom/home'
            with self.session.get(welcome, allow_redirects=False) as resp:
                if resp.status_code==200:
                    self._Session = self.session
                    print('登陆缓存加载成功')
                    return
                print('cookie加载有问题')
                os.remove('Session')
        if not os.path.exists('Session'):
            if self.login(self.passwd, self.user):
                self._Session = self.session
                return
            print('登陆出错，请排查相应问题')
            self._Session = requests.session()

    def login(self, secret, account):
        '''动态变化的参数,指向验证码和登录'''
        print('cadfa')
        while True:
            index_url = 'https://www.chinabidding.cn/cblcn/member.login/login'
            # 获取登录时需要用到的randomID
            login_page = self.session.get(index_url, headers=self.headers)
            html = login_page.text
            pattern = r'login/captcha\?randomID=(.*?)"'
            randomID = re.findall(pattern, html)[0]

            self.headers["X-Requested-With"] = "XMLHttpRequest"
            postdata = {
                'name': account,
                'password': secret,
                'url': '',
                'yzm': '',
                'randomID': randomID,
                't':'1547132532835',
                }
            postdata["yzm"] = self.get_captcha(randomID)
            post_url = 'https://www.chinabidding.cn/cblcn/member.login/logincheck'
            login_page = self.session.post(post_url, data=postdata, headers=self.headers)
            with open('Session', 'wb') as f:
                pickle.dump(self.session, f)
            print('用户登陆成功！',login_page.status_code)
            return login_page.status_code


class Crawl(Login):
    '''爬取项目链接列表'''
    def __init__(self):
        #导入登陆父类初始化函数
        Login.__init__(self)
        self.search = 'http://projects.rccchina.com/projects/search'
        self.search_result = 'http://projects.rccchina.com/projects/search_result'

    def index_page(self,**kw):
        '''高级搜索界面模拟'''
        page = 1
        total_sre = re.compile(r'div id="nav_bar_bottom"[\S\s]*?共(\d+)页')
        pagesize = 'http://projects.rccchina.com/projects/set_project_per_page/?_ruid=%s&num=100' % self.logined.cookies.get('_ruid')
        self.logined.get(pagesize)
        self.logined.get(self.search)
        with self.logined.post(self.search_result,**kw) as resp:
            resp.encoding='utf-8'
            pagetext = resp.text
            yield pagetext
        total = int(''.join(total_sre.findall(pagetext) or [1]))        
        while page<total:
            page += 1
            params = {'only_firm': '', 'page': page, 'project_from_list': 0,}
            with self.logined.get(self.search_result,params=params) as resp:
                resp.encoding='utf-8'
                pagetext = resp.text
                yield pagetext

    def get_detail(self, href, **kw):
        '''获取招中标页面信息'''
        # href = 'http://192.168.99.100:8050/render.html?url=' + href
        with self.logined.get(href, **kw) as detail:
            detail.encoding = 'utf-8'
            return detail.text


class Processing():

    def first_2_str(self, mylist):
        '''返回列表元素连接的字符串，如果列表为空，返回空字符串
        函数的作用是防止空列表抛出查询错误'''
        return ''.join(mylist).strip() #(mylist or [''])[0].strip()

    def search_result_parse(self, pagetext):
        '''解析搜索结果页面
        param:pagetext是结果网页的文本对象'''

        html = etree.HTML(pagetext)
        tr_list = html.xpath(r'//table[@id="project_list"]/tr[@bgcolor]')
        for tr in tr_list:
            #一个公告条目tr标签信息的提取
            show = 'http://projects.rccchina.com'
            keys=('项目ID', '项目名称', '造价(百万)', '项目阶段', '省份', '公布时间', '项目链接')
            values = []
            _id_cost_stage_city = [self.first_2_str(tr.xpath(r'td[%d]/text()'%x)) for x in [2,4,5,6]]
            multi_td = tr.xpath(r'td[3]/a[contains(@class,"pn")]')[0]
            name = self.first_2_str(multi_td.xpath(r'text()'))
            href = self.first_2_str(multi_td.xpath(r'@href'))
            href = show+href if href else href
            t = self.first_2_str(tr.xpath(r'td[last()]/span/text()'))
            values.extend(_id_cost_stage_city)
            values.append(t)
            values.append(href)
            values.insert(1,name)
            yield dict(zip(keys,values))

    def removebiaodian(self, str_):
        #去掉末尾的句号
        biaodian_sre = re.compile(r'。$')
        return biaodian_sre.sub('', str_.strip())

    def project_parse(self, pagetext):
        '''解析工程条目页面
        param:pagetext是工程网页的文本对象'''
        worktime_sre = re.compile(r'项目工期\s*?</div>[\S\s]*?>工程开始日期（主体开工）：(.*?)工程结束日期（交付使用）：(.*?)<')    
        html = etree.HTML(pagetext)
        #基础信息
        item = {}
        name = self.first_2_str(html.xpath(r'//div[@class="p-header"]/div[@class="p-title"]/span/text()'))
        address = self.first_2_str(html.xpath(r'//div[@class="p-header"]/div[@class="address no-copy"]/span/text()'))
        item['项目名称'] = name
        item['项目地址'] = address

        #表信息
        table_th = html.xpath(r'//table[@class="p-basicinfo"]/tr/th')
        table_key = [self.first_2_str(th.xpath(r'text()')) for th in table_th]

        table_value = [self.first_2_str(td.xpath(r'.//text()')) for td in html.xpath(r'//table[@class="p-basicinfo"]/tr/td')]
        table = dict(zip(table_key,table_value))
        
        #项目概况
        desc = html.xpath(r'//div[@class="project_desc"]//text()')
        table['项目概况'] = ''.join(desc).strip()
        beginendtime = worktime_sre.search(pagetext)
        if beginendtime:
            table['开工日期'] = self.removebiaodian(beginendtime.group(1))
            table['预计交付日期'] = self.removebiaodian(beginendtime.group(2))

        item.update(table)
        
        #有的有外资参与的备注，与外资参与键值不同，统一一下
        wzcybz = item.get('外资参与（外资参与情况备注）', '')
        if wzcybz:
            if not item.get('外资参与'):
                item['外资参与'] = wzcybz
        
        return item

    def de_duplication(self, dict_list):
        #字典列表去重
        _json_list = [json.dumps(item) for item in dict_list]
        temp_list = sorted(set(_json_list),key=_json_list.index)
        final_list = [json.loads(newitem) for newitem in temp_list]
        return final_list

    def save(self, itemlist, tabletitle, filename):

        filename = filename or '楼宇数据'

        wb = Workbook()
        ws = wb.active

        ws.append(tabletitle)
        for item in itemlist:
            value_list = list(item.values())
            ws.append(value_list)

        wb.save(filename+'.xlsx')

    def main(self):
        # needkeys = NEEDKEYS[:] or None
        # tabletitle = TABLETITLE[:] or None
        # filename = FILE_NAME or None
        # 新建瑞达恒爬虫实例
        caizhao = Crawl()
        # caizhao.login('密', '名')
        print(caizhao.get_detail('https://www.chinabidding.cn/zbgg/exKWk.html'))
        # 从搜索结果中遍历页面，解析出工程链接列表
        # href_list = pd.read_csv('caizhao_whole.csv', encoding='gb18030')['链接'].dropna()
        # href_list = ['https://www.chinabidding.cn/zbgg/exKWk.html']
        # biddings = Group().imap(caizhao.get_detail, href_list, maxsize=200)
        # raw_list = [self.project_parse(bidding) for bidding in biddings]

        # if not needkeys:
        #     setkey = set()
        #     for raw in raw_list:
        #         setkey.update(list(raw.keys))
        #     else:
        #         needkeys = sorted(list(setkey))

        # need_value_list = [{k: item.get(k, '') for k in needkeys} for item in raw_list]

        # #project_list = de_duplication(need_value_list)

        # if not tabletitle:
        #     tabletitle = needkeys
        # self.save(need_value_list, tabletitle, filename)
        # print(biddings)


if __name__ == '__main__':
    Processing().main()