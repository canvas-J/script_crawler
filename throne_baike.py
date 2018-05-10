# -*- coding:utf-8 -*-
import requests
import time
import re

class Tool:
    removeImg = re.compile('<a class=.*?px;">')
    removeAddr = re.compile('<a.*?>|</a>')
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    replaceTD= re.compile('<td>')
    replacePara = re.compile('<p.*?>')
    replaceBR = re.compile('<br><br>|<br>')
    removeExtraTag = re.compile('<.*?>')
    def replace(self, x):
        x = re.sub(self.removeImg, "", x)
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.replaceLine, "\n", x)
        x = re.sub(self.replaceTD, "\t", x)
        x = re.sub(self.replacePara, "\n    ", x)
        x = re.sub(self.replaceBR, "\n", x)
        x = re.sub(self.removeExtraTag, "", x)
        return x.rstrip()

class THRONE:

    def __init__(self):
        self.tool = Tool()
        self.li = ['一季/10497381','二季/7227318','三季/9701225','四季/7108940','五季/15870653','六季/15884978','七季/15884938']
        self.url = 'https://baike.baidu.com/item/权力的游戏第'
        self.file = None

    def getPage(self, c):
        try:
            headers = {"User-Agent":"Mozilla/5.0(Macintosh;IntelMacOSX10_7_0)AppleWebKit/535.11(KHTML,likeGecko)Chrome/17.0.963.56Safari/535.11",
                        "User-Agent":"Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;360SE)",
                        "User-Agent":"Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;TheWorld)",
                        "User-Agent":"Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;Trident/4.0;SE2.XMetaSr1.0;SE2.XMetaSr1.0;.NETCLR2.0.50727;SE2.XMetaSr1.0)",
                        "User-Agent":"Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1)",
                        "User-Agent":"Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;AvantBrowser)",
                        "User-Agent":"Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1)"}
            url = self.url + "{}?fr=aladdin".format(c)
            r = requests.get(url = url, headers = headers)
            text = r.content.decode('utf-8')
            return text
        except:
            print("网站拦截？")

    def findItems0(self, c):
        pattern0 = re.compile('<dd class="basicInfo-item value">(.*?)</dd>',re.S)
        text = self.getPage(c)
        r0 = re.findall(pattern0, text)
        return r0[0]

    def findItems1(self, c):
        pattern1 = re.compile('<dl>.*?<dt>.*?<span>(.*?)</span>.*?<span>(.*?)</span>.*?<span>(.*?)</span>.*?<span>(.*?)</span>.*?<span>(.*?)</span>.*?<span>(.*?)</span>.*?<span>(.*?)</span>.*?<dl>.*?<dt>.*?<span>(.*?)</span>.*?<span>(.*?)</span>.*?<span>(.*?)</span>.*?<span>(.*?)</span>.*?<span>(.*?)</span>',re.S)
        pattern2 = re.compile('<dl>.*?<dt>.*?</span>.*?<dd>(.*?)</dd>.*?</span>.*?<dd>(.*?)</dd>.*?</span>.*?<dd>(.*?)</dd>.*?</span>.*?<dd>(.*?)</dd>.*?</span>.*?<dd>(.*?)</dd>.*?</span>.*?<dd>(.*?)</dd>.*?<dl>.*?<dt>.*?</span>.*?<dd>(.*?)</dd>.*?</span>.*?<dd>(.*?)</dd>.*?</span>.*?<dd>(.*?)</dd>.*?</span>.*?<dd>(.*?)</dd>.*?</span>.*?<dd>(.*?)</dd>',re.S)
        # 第七季网页，第一季的也不一样，但简单些
        # pattern1 = re.compile('<dl>.*?<dt>.*?<span>(.*?)</span>.*?<span>(.*?)</span>.*?<span>(.*?)</span>.*?<span>(.*?)</span>.*?<span>(.*?)</span>.*?<span>(.*?)</span>.*?<span>(.*?)</span>.*?<dl>.*?<dt>.*?<span>(.*?)</span>.*?<span>(.*?)</span>',re.S)
        # pattern2 = re.compile('<dl>.*?<dt>.*?</span>.*?<dd>(.*?)</dd>.*?</span>.*?<dd>(.*?)</dd>.*?</span>.*?<dd>(.*?)</dd>.*?</span>.*?<dd>(.*?)</dd>.*?</span>.*?<dd>(.*?)</dd>.*?</span>.*?<dd>(.*?)</dd>.*?<dl>.*?<dt>.*?</span>.*?<dd>(.*?)</dd>.*?</span>.*?<dd>(.*?)</dd>',re.S)
        text = self.getPage(c)
        r1 = re.findall(pattern1, text)
        r2 = re.findall(pattern2, text)
        r = [r1, r2]
        return r

    def main(self):
        for i in range(0, 6):
            c = self.li[i]
            r0 = self.findItems0(c)
            r0 = self.tool.replace(r0)
            print(r0)
            r = self.findItems1(c)
            for j in range(10):
                a = r[0][0][j+2] + "\n"
                b = r[1][0][j+1] + "\n"
                b = self.tool.replace(b)
                with open("img/throne/{}.txt".format(r0),"a+") as self.file:
                    self.file.write(a+"\n")
                    self.file.write(b+"\n\n")
                
            print("本季内容已保存！共{}条内容".format(j + 1))
            time.sleep(2)

spider = THRONE()
spider.main()
