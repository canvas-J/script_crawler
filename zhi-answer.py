# -*- coding=utf-8 -*-
import os, datetime, re, logging, traceback
from openpyxl import Workbook
from zhihu_oauth import ZhihuClient
from zhihu_oauth.exception import NeedCaptchaException

question_id = input('请输入问题id号，获取所有答案：')
TOKEN_FILE = 'token.pkl'
client = ZhihuClient()

if os.path.isfile(TOKEN_FILE):
    client.load_token(TOKEN_FILE)
else:
    try:
        client.login('email_or_phone', 'password')
    except NeedCaptchaException:
        with open('a.gif', 'wb') as f:
            f.write(client.get_captcha())
        captcha = input('please input captcha:')
        client.login('email_or_phone', 'password', captcha)
    client.save_token(TOKEN_FILE)

question = client.question(int(question_id))
print(question.title)
wb = Workbook()
sheet = wb.active
sheet.title = "知乎"
item_name = ['time_now', 'content', 'author', 'gender', 'loc', 'business', 'company', 'job', 'created_time', 'updated_time', 'voteup_count', 'comment_count', 'thanks_count']
for j,title in enumerate(item_name):
    sheet.cell(row=1, column=j+1).value = title
num = 0
for answer in question.answers:
    num += 1
    item_data = [datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')]
    # item_data.append([answer.author.name, answer.can_comment.status, answer.comment_count, answer.comment_permission, answer.content,
    #         answer.created_time, answer.excerpt, answer.is_copyable, answer.is_mine, answer.question, answer.suggest_edit.reason,
    #         answer.thanks_count, answer.updated_time, answer.voteup_count, answer.collections, answer.comments, answer.voters
    #         ])
    gender_dict = {'0': '女', '1': '男', '-1': '不详'}
    if answer.author.gender != None:
        gender = gender_dict[str(answer.author.gender)]
    else:
        gender = '不详'
    loc = ''
    if answer.author.locations:
        for location in answer.author.locations:
            loc += location.name
    company = ''
    job = ''
    if answer.author.employments:
        for employment in answer.author.employments:
            if 'company' in employment:
                company += employment.company.name
            if 'job' in employment:
                job += employment.job.name
    if answer.author.business:
        business = answer.author.business.name
    else:
        business = ''
    try:
        item_data += [re.compile(r'<.*?>', re.S).sub('', answer.content), answer.author.name, gender, loc, business, company, job,
                datetime.datetime.fromtimestamp(answer.created_time), datetime.datetime.fromtimestamp(answer.updated_time),
                answer.voteup_count, answer.comment_count, answer.thanks_count
                ]
    except:
        logging.error(question.title+'******'+answer.author.name+'\n'+'-'*60+'\n'+traceback.format_exc()+'-'*60+'\n')
    # print(answer.author.name, answer.voteup_count)
    finally:
        sheet.append(item_data)
        # answer.save(question.title)
    if num % 10 == 0:
        wb.save('知乎回答-{}.xlsx'.format('护肤'))