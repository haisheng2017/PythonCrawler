# -*- coding: UTF-8 -*-
import re

import phoenixdb
import phoenixdb.cursor

import datetime

import time
import datetime
import requests
import re
import phoenixdb
import phoenixdb.cursor
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
#
# str = "2018-06-21"
# database_url = 'http://node1:8765/'
# phoenix_conn = phoenixdb.connect(database_url, autocommit=True)
# cursor = phoenix_conn.cursor(cursor_factory=phoenixdb.cursor.DictCursor)

# try:
#     chrome_options = Options()
#     chrome_options.add_argument('--headless')
#     chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(executable_path=r'chromedriver.exe')
driver.get("http://www.baidu.com")
    # entity={'ID': 28, 'NAME': '元旦', 'DATE_END': '2018-01-01', 'DATE_START': '2017-12-30'}
    # cursor.execute("UPSERT INTO THIRDWORK_VOCATION(ID,NAME, DATE_START,DATE_END) VALUES (?,?,TO_DATE(?,'yyyy-MM-dd'),TO_DATE(?,'yyyy-MM-dd'))",
    #                (entity['ID'],entity['NAME'],entity['DATE_START'],entity['DATE_END']))
    #
    # print(cursor.rowcount)
#     id=1
#     # data=(24702, '动力电池装配联合厂房等5项（动力电池工厂建设项目）', '[2018]施[经]建字0012号', '经济技术开发区', '北京奔驰汽车有限公司', '56347.33', '2018-03-20', '亦庄开发区N13M1地块', '北京建工集团有限责任公司', '北京京龙工程项目管理有限公司', '北京市工业设计研究院有限公司', '600003205', '徐和谊', '北京市经济技术开发区建设发展局', '本证自发证之日起三个月内应予施工，逾期应办理延期手续，不办理延期或延期次数、时间超过法定时间的，本证自行废止。', '')
#     # cursor.execute("UPSERT INTO THIRDWORK_PERMIT(ID,PROJECTNAME,PERMITNUM,DISTRICT,BUILDER,SCALE,PERMITDATE,ADDRESS,CONSTRUCTIONUNIT,SUPERVISEUNIT,DESIGNUNIT,ADMINISTRATIONCODE,REPRESENTATIVENAME,PERMITUNIT,PERMITDEADLINE,CERTIFICATESTATUS) VALUES (?, ?, ?, ?,?, ?, TO_DATE(?,'yyyy-MM-dd'), ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
#     # cursor.execute("SELECT * FROM test.python")
#     # print(cursor.rowcount)
#     # cursor.execute(
#     #     "SELECT * FROM THIRDWORK_FINISH ORDER BY case when FINISHDATE is null then 1 else 0 end asc ,FINISHDATE desc limit 1")
#     # date = cursor.fetchone()['FINISHDATE'].strftime('%Y-%m-%d')
#     # cursor.execute("SELECT * FROM THIRDWORK_FINISH ORDER BY id desc limit 1")
#     # id = cursor.fetchone()['ID']
#     # print(date,id)
#     # data=[]
#     # data.append(1)
#     # data.append(1)
#     # data.append(1)
#     # data.append(1)
#     # print(data[0],data[-1])
#     # cursor.execute("SELECT * FROM THIRDWORK_PERMIT ORDER BY case when PERMITDATE is null then 1 else 0 end asc ,PERMITDATE desc limit 1")
#     # date=cursor.fetchone()['PERMITDATE'].strftime('%Y-%m-%d')
#     # cursor.execute("SELECT * FROM THIRDWORK_PERMIT ORDER BY id desc limit 1")
#     # id=cursor.fetchone()['ID']
#     # print(id,date)
#     # print(str>date)
#     str = '''根据国务院《关于修改〈全国年节及纪念日放假办法〉的决定》，为便于各地区、各部门及早合理安排节假日旅游、交通运输、生产经营等有关工作，经国务院批准，现将2012年元旦、春节、清明节、劳动节、端午节、中秋节和国庆节放假调休日期的具体安排通知如下。
#
# 一、元旦：2012年1月1日至3日放假调休，共3天。2011年12月31日（星期六）上班。
#
# 二、春节：1月22日至28日放假调休，共7天。1月21日（星期六）、1月29日（星期日）上班。
#
# 三、清明节：4月2日至4日放假调休，共3天。3月31日（星期六）、4月1日（星期日）上班。
#
# 四、劳动节：4月29日至5月1日放假调休，共3天。4月28日（星期六）上班。
#
# 五、端午节：6月22日至24日放假公休，共3天。
#
# 六、中秋节、国庆节：9月30日至10月7日放假调休，共8天。9月29日（星期六）上班。
#
# 节假日期间，各地区、各部门要妥善安排好值班和安全、保卫等工作，遇有重大突发事件发生，要按规定及时报告并妥善处置，确保人民群众祥和平安度过节日假期。
#     '''
# #     str = '''
# #     各省、自治区、直辖市人民政府，国务院各部委、各直属机构：
# #
# # 经国务院批准，现将2014年元旦、春节、清明节、劳动节、端午节、中秋节和国庆节放假调休日期的具体安排通知如下。
# #
# # 一、元旦：1月1日放假1天。
# #
# # 二、春节：1月31日至2月6日放假调休，共7天。1月26日（星期日）、2月8日（星期六）上班。
# #
# # 三、清明节：4月5日放假，4月7日（星期一）补休。
# #
# # 四、劳动节：5月1日至3日放假调休，共3天。5月4日（星期日）上班。
# #
# # 五、端午节：6月2日放假，与周末连休。
# #
# # 六、中秋节：9月8日放假，与周末连休。
# #
# # 七、国庆节：10月1日至7日放假调休，共7天。9月28日（星期日）、10月11日（星期六）上班。
# #
# # 节假日期间，各地区、各部门要妥善安排好值班和安全、保卫等工作，遇有重大突发事件，要按规定及时报告并妥善处置，确保人民群众祥和平安度过节日假期。'''
#
#     text = str.split()
#
#     number = r"^[一、|二、|三、|四、|五、|六、|七、|八、|九、|十、].*"
#     nextYear = '2012'
#     # print(text)
#     pattern = re.compile(number)
#     parseList = []
#     for t in text:
#         if re.match(pattern, t):
#             parseList.append(t)
#     # print(parseList)
#
#     weekend = re.compile("周末连休")
#     rest = re.compile("补休")
#     period = re.compile("至")
#     single=re.compile("放假")
#
#     mdPattern = re.compile("[0-9]{1,2}月[0-9]{1,2}日")
#     dPattern = re.compile("[0-9]{1,2}日")
#
#     for l in parseList:
#         id=id+1
#         entity = {}
#         entity['id']=id
#         result = l.split('：')
#         # print(result[-1])
#         if result is None or len(result) < 2:
#             print("跳过了很多东西")
#             continue
#         # print(result[0].split('、')[1:])
#         name='、'
#         entity['NAME'] = name.join(result[0].split('、')[1:])
#         # 周末连休判断
#         if re.search(weekend, result[-1]):
#             match = re.findall(mdPattern, result[-1])
#             if match and len(match) > 0:
#                 y = datetime.datetime.strptime(nextYear + "年" + match[0], '%Y年%m月%d日')
#                 # print(y, y.strftime("%w"))
#                 if y.strftime("%w") == '1':
#                     entity['DATE_END'] = y.strftime('%Y-%m-%d')
#                     y = y - datetime.timedelta(days=2)
#                     entity['DATE_START'] = y.strftime('%Y-%m-%d')
#                 elif y.strftime("%w") == '5':
#                     entity['DATE_START'] = y.strftime('%Y-%m-%d')
#                     y = y + datetime.timedelta(days=2)
#                     entity['DATE_END'] = y.strftime('%Y-%m-%d')
#                 print(entity)
#         # 补休判断
#         elif re.search(rest, result[-1]):
#             match = re.findall(mdPattern, result[-1])
#             if match and len(match) > 0:
#                 y = datetime.datetime.strptime(nextYear + "年" + match[-1], '%Y年%m月%d日')
#                 # print(y, y.strftime("%w"))
#                 if y.strftime("%w") == '1':
#                     entity['DATE_END'] = y.strftime('%Y-%m-%d')
#                     y = y - datetime.timedelta(days=2)
#                     entity['DATE_START'] = y.strftime('%Y-%m-%d')
#                 elif y.strftime("%w") == '5':
#                     entity['DATE_START'] = y.strftime('%Y-%m-%d')
#                     y = y + datetime.timedelta(days=2)
#                     entity['DATE_END'] = y.strftime('%Y-%m-%d')
#             print(entity)
#         # 放假调休
#         elif re.search(period,result[-1]):
#             days=result[-1].split("，")[0]
#             match = re.findall(mdPattern, days)
#             #不同月
#             if match and len(match)>1 :
#                 y = datetime.datetime.strptime(nextYear + "年" + match[0], '%Y年%m月%d日')
#                 entity['DATE_START'] = y.strftime('%Y-%m-%d')
#                 y = datetime.datetime.strptime(nextYear + "年" + match[1], '%Y年%m月%d日')
#                 entity['DATE_END'] = y.strftime('%Y-%m-%d')
#             # 同一个月份
#             elif match and len(match)==1:
#                 day=re.findall(dPattern,days)
#                 if day is None or len(day) <1 : continue
#                 y = datetime.datetime.strptime(nextYear + "年" + match[0], '%Y年%m月%d日')
#                 entity['DATE_START'] = y.strftime('%Y-%m-%d')
#                 y = datetime.datetime.strptime(nextYear + "年" + match[0].split("月")[0]+"月"+day[1], '%Y年%m月%d日')
#                 entity['DATE_END'] = y.strftime('%Y-%m-%d')
#             print(entity)
#         # 其他情况 ：单天放假
#         elif re.search(single,result[-1]):
#             match = re.findall(mdPattern, result[-1])
#             if match and len(match)>0 :
#                 y = datetime.datetime.strptime(nextYear + "年" + match[0], '%Y年%m月%d日')
#                 entity['DATE_START'] = y.strftime('%Y-%m-%d')
#                 entity['DATE_END'] = y.strftime('%Y-%m-%d')
#             print(entity)
#         else:
#             print("国务院可能又修改放假文件格式了")
# finally:
    # cursor.close()
    # phoenix_conn.close()
