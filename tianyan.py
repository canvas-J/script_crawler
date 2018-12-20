import requests, time
from bs4 import BeautifulSoup


def company_url(names):
    prise_id = []
    for name in names:
        url = 'https://www.tianyancha.com/search?key={0}'.format(name)
        html = requests.get(url, headers=headers).text
        #html = requests.get(url, headers=headers,proxies=proxies).text#加IP的情况
        soup = BeautifulSoup(html, 'lxml')
        infs = soup.find_all('div', class_='search-item')
        if not infs:
            print('抱歉没有找到%s的相关信息' % name)
            continue
        for inf in infs:
            url = inf.find('div', class_='search-result-single').get('data-id')
            prise_id.append(url)
    return prise_id

def change(content):
    dit={'4':'1',
        '6':'2',
        '1':'3',
        '8':'4',
        '9':'6',
        '2':'7',
        '7':'8',
        '3':'9','将':'人'
        }
    sent=''
    for i in content:
        try:
            sent += dit[i]
        except KeyError:
            sent += i
    return sent

def company_infs(ids):
    for enterprise in ids:
        url='https://www.tianyancha.com/company/{0}'.format(enterprise)
        html=requests.get(url,headers=headers).text
        # html = requests.get(url, headers=headers,proxies=proxies).text#加IP的情况
        soup=BeautifulSoup(html,'lxml')
        data={}
        number=soup.find_all('text',class_='tyc-num lh24')
        data['name']=soup.find('div',class_='header').find('h1',class_='name').text
        data['法人代表']=soup.find('div',class_='name').find('a',class_='link-click').text
        data['注册资本']=change(number[0].text)
        data['注册时间']=change(number[1].text)
        if soup.find('div',class_='num-opening'):
            data['公司状态']=soup.find('div',class_='num-opening').text
        elif soup.find('div',class_='num-cancel'):
            data['公司状态']=soup.find('div',class_='num-cancel').text
        someinfs=soup.find('table',class_='table -striped-col -border-top-none').find_all('tr')
        data['工商注册号']=someinfs[0].find('td',width='30%').text
        data['组织机构代码']=someinfs[0].find('td',width='20%').text
        data['统一社会信用代码']=someinfs[1].find_all('td')[1].text
        data['公司类型']=someinfs[1].find_all('td')[3].text
        data['纳税人识别号']=someinfs[2].find_all('td')[1].text
        data['行业']=someinfs[2].find_all('td')[3].text
        data['营业期限']=someinfs[3].find_all('td')[1].text
        data['核准日期'] = change(someinfs[3].find_all('td')[3].text)
        data['实缴资本']=someinfs[5].find_all('td')[1].text
        data['登记机关']=someinfs[5].find_all('td')[3].text
        data['参保人数']=someinfs[6].find_all('td')[1].text
        data['英文名称']=someinfs[6].find_all('td')[3].text
        data['地址']=someinfs[7].find_all('td')[1].text
        data['经营范围'] = change(soup.find('span',class_='js-full-container hidden').text)
        if not data['经营范围']:
            data['经营范围']=change(soup.find('span',class_='js-split-container').text)
        print(data)


if __name__=='__main__':
    # 加登陆Cookie，经营范围不需要解密，不加登陆Cookie,经营范围需要解密
    headers={'Cookie': 'aliyungf_tc=AQAAAMD6yxtABAsAOBvidHEDjDgYC8K/; csrfToken=sMGZJR75_4EY77QERKmSXWTT; TYCID=2889c560041611e9bdcf3d09c4a1e902; undefined=2889c560041611e9bdcf3d09c4a1e902; ssuid=1352985371; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1545282887; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1545283373; bannerFlag=true; token=662565c9dde84c9bb3534cd1c5b9211b; _utm=955d67b236e841fab86d5a31953b5fbb; tyc-user-info=%257B%2522claimEditPoint%2522%253A%25220%2522%252C%2522myQuestionCount%2522%253A%25220%2522%252C%2522explainPoint%2522%253A%25220%2522%252C%2522nickname%2522%253A%2522%25E5%25A7%259A%25E5%25BF%2585%25E8%25BE%25BE-6h2%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522nicknameSup%2522%253A%25226h2%2522%252C%2522state%2522%253A%25220%2522%252C%2522announcementPoint%2522%253A%25220%2522%252C%2522nicknameOriginal%2522%253A%2522%25E5%25A7%259A%25E5%25BF%2585%25E8%25BE%25BE%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522discussCommendCount%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%25220%2522%252C%2522onum%2522%253A%25220%2522%252C%2522claimPoint%2522%253A%25220%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNzY4ODkzMzE1OCIsImlhdCI6MTU0NTI4MzM2OCwiZXhwIjoxNTYwODM1MzY4fQ.CoIwvzPRSmlK7ELUIOO2kNAm1I9O4DBtl17KG0gbq1umMuLudKmDmOMj3n20Zm_9EC5ARfHix7Wz7yw8hi--NA%2522%252C%2522pleaseAnswerCount%2522%253A%25220%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252217688933158%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNzY4ODkzMzE1OCIsImlhdCI6MTU0NTI4MzM2OCwiZXhwIjoxNTYwODM1MzY4fQ.CoIwvzPRSmlK7ELUIOO2kNAm1I9O4DBtl17KG0gbq1umMuLudKmDmOMj3n20Zm_9EC5ARfHix7Wz7yw8hi--NA',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'www.tianyancha.com',
            'Referer': 'https://www.tianyancha.com/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
    names=['上海复硕正态管理咨询有限公司']
    ids=company_url(names)
    company_infs(ids)