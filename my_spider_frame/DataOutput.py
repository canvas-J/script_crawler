#coding:utf-8
import codecs       #  自然语言编码转换

class DataOutput(object):

    def __init__(self):
        self.datas=[]

    #　把对象序列化为列表
    def data_to_list(self, data):
        if data is None:
            return
        self.datas.append(data)

    # 输出为html文档，方便阅读
    def output_html(self):
        fout = codecs.open('baike.html', 'w', encoding='utf-8')
        fout.write("<html>")
        fout.write("<head><meta charset='utf-8'/></head>")
        fout.write("<body>")
        fout.write("<table>")
        for data in self.datas:
            fout.write("<tr>")
            fout.write("<td>%s</td>"%data['url'])
            fout.write("<td>%s</td>"%data['title'])
            fout.write("<td>%s</td>"%data['summary'])
            fout.write("</tr>")

        fout.write("</table>")
        fout.write("</body>")
        fout.write("</html>")
        fout.close()

