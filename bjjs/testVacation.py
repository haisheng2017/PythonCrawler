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

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    # "Cookie": "user_sid=e8b24cae8b664079a20753c8f583e3d3; searchid=aee087de678941298ce2f22d1530fae3; pageUrl=http%3A%2F%2Fsearch.www.gov.cn%2Fsearch%2Ffw%2FcateSearch.do%3Fwebid%3D1%26q%3D%25E8%258A%2582%25E5%2581%2587%25E6%2597%25A5%26p%3D1%26pg%3D20%26category%3Dzcwj; JSESSIONID=4A25543E45E910EB25B266EA94766C11; __auc=511f3e0e163a48886c7e8735518; allmobilize=mobile; __asc=b650a546164254cf82e3f87d8a2; SERVERID=4cb9438f97056e94080e20183e1ef2a6|1529634194|1529634171",
    "Host": "search.www.gov.cn",
    "Referer": "http://www.gov.cn/fuwu/index.htm",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36",
}

url = r"http://search.www.gov.cn/search/fw/cateSearch.do?webid=1&category=zcwj&q=%E8%8A%82%E5%81%87%E6%97%A5"

database_url = 'http://node1:8765/'
phoenix_conn = phoenixdb.connect(database_url, autocommit=True)
cursor = phoenix_conn.cursor(cursor_factory=phoenixdb.cursor.DictCursor)

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(executable_path=r'D:\chromedriver_win32\chromedriver.exe',chrome_options=chrome_options)
# driver = webdriver.PhantomJS(executable_path=r'D:\phantomjs-2.1.1-windows\bin\phantomjs')
# driver = webdriver.Chrome(executable_path=r'D:\chromedriver_win32\chromedriver.exe')
try:
    returnNumber=0
    cursor.execute("SELECT * FROM THIRDWORK_VOCATION ORDER BY date_start desc limit 1")
    date = cursor.fetchone()['DATE_START'].strftime('%Y')
    cursor.execute("SELECT * FROM THIRDWORK_VOCATION ORDER BY id desc limit 1")
    id = cursor.fetchone()['ID']
    print(date, id)
    # driver.get("http://pythonscraping.com/pages/javascript/ajaxDemo.html")
    # time.sleep(3)
    # print(driver.find_element_by_id('content').text)
    # print(driver.page_source)
    # driver.close()
    # flag = True
    nextYear=str((int(date) + 1))
    keyword = r"^国务院办公厅.*" + nextYear + ".*节假日.*"
    number = r"^[一、|二、|三、|四、|五、|六、|七、|八、|九、|十、].*"
    print(keyword)
    # driver.find_element_by_css_selector('.cate-box-policy cate-group-infos')

    try:
        driver.get(url)
        urlList = ''
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul.cate-box-policy.cate-group-infos")))
        list = element.find_elements_by_tag_name('li')
        pattern = re.compile(keyword)
        for li in list:
            div = li.find_element_by_css_selector('div.news-title')
            print(div.text)
            if re.match(pattern, div.text):
                aTag = li.find_element_by_tag_name('a')
                urlList = (aTag.get_attribute('href'))
            else:
                print("匹配不成功")
        if urlList  and urlList != '':
            driver.get(urlList)
            td = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "td.b12c")))
            text = td.text.split()
            pattern = re.compile(number)
            parseList = []
            for t in text:
                if re.match(pattern, t):
                    parseList.append(t)


            weekend = re.compile("周末连休")
            rest = re.compile("补休")
            period = re.compile("至")
            single=re.compile("放假")

            mdPattern = re.compile("[0-9]{1,2}月[0-9]{1,2}日")
            dPattern = re.compile("[0-9]{1,2}日")

            for l in parseList:
                id=id+1
                entity = {}
                entity['ID']=id
                result = l.split('：')
                # print(result[-1])
                if result is None or len(result) < 2:
                    print("跳过了很多东西")
                    continue
                # print(result[0].split('、')[1:])
                name='、'
                entity['NAME'] = name.join(result[0].split('、')[1:])
                # 周末连休判断
                if re.search(weekend, result[-1]):
                    match = re.findall(mdPattern, result[-1])
                    if match and len(match) > 0:
                        y = datetime.datetime.strptime(nextYear + "年" + match[0], '%Y年%m月%d日')
                        # print(y, y.strftime("%w"))
                        if y.strftime("%w") == '1':
                            entity['DATE_END'] = y.strftime('%Y-%m-%d')
                            y = y - datetime.timedelta(days=2)
                            entity['DATE_START'] = y.strftime('%Y-%m-%d')
                        elif y.strftime("%w") == '5':
                            entity['DATE_START'] = y.strftime('%Y-%m-%d')
                            y = y + datetime.timedelta(days=2)
                            entity['DATE_END'] = y.strftime('%Y-%m-%d')
                        print(entity)
                # 补休判断
                elif re.search(rest, result[-1]):
                    match = re.findall(mdPattern, result[-1])
                    if match and len(match) > 0:
                        y = datetime.datetime.strptime(nextYear + "年" + match[-1], '%Y年%m月%d日')
                        # print(y, y.strftime("%w"))
                        if y.strftime("%w") == '1':
                            entity['DATE_END'] = y.strftime('%Y-%m-%d')
                            y = y - datetime.timedelta(days=2)
                            entity['DATE_START'] = y.strftime('%Y-%m-%d')
                        elif y.strftime("%w") == '5':
                            entity['DATE_START'] = y.strftime('%Y-%m-%d')
                            y = y + datetime.timedelta(days=2)
                            entity['DATE_END'] = y.strftime('%Y-%m-%d')
                    print(entity)
                # 放假调休
                elif re.search(period,result[-1]):
                    days=result[-1].split("，")[0]
                    match = re.findall(mdPattern, days)
                    #不同月
                    if match and len(match)>1 :
                        y = datetime.datetime.strptime(nextYear + "年" + match[0], '%Y年%m月%d日')
                        entity['DATE_START'] = y.strftime('%Y-%m-%d')
                        y = datetime.datetime.strptime(nextYear + "年" + match[1], '%Y年%m月%d日')
                        entity['DATE_END'] = y.strftime('%Y-%m-%d')
                    # 同一个月份
                    elif match and len(match)==1:
                        day=re.findall(dPattern,days)
                        if day is None or len(day) <1 : continue
                        y = datetime.datetime.strptime(nextYear + "年" + match[0], '%Y年%m月%d日')
                        entity['DATE_START'] = y.strftime('%Y-%m-%d')
                        y = datetime.datetime.strptime(nextYear + "年" + match[0].split("月")[0]+"月"+day[1], '%Y年%m月%d日')
                        entity['DATE_END'] = y.strftime('%Y-%m-%d')
                    print(entity)
                # 其他情况 ：单天放假
                elif re.search(single,result[-1]):
                    match = re.findall(mdPattern, result[-1])
                    if match and len(match)>0 :
                        y = datetime.datetime.strptime(nextYear + "年" + match[0], '%Y年%m月%d日')
                        entity['DATE_START'] = y.strftime('%Y-%m-%d')
                        entity['DATE_END'] = y.strftime('%Y-%m-%d')
                    print(entity)
                else:
                    print("国务院可能又修改放假文件格式了")
                cursor.execute("UPSERT INTO THIRDWORK_VOCATION(ID,NAME, DATE_START,DATE_END) VALUES (?,?,TO_DATE(?,'yyyy-MM-dd'),TO_DATE(?,'yyyy-MM-dd'))",
                               (entity['ID'],entity['NAME'],entity['DATE_START'],entity['DATE_END']))
                returnNumber=returnNumber+cursor.rowcount
    finally:
        driver.quit()
        # print(driver.find_element_by_css_selector('.fwbanner_wrap').text)
    # driver.close()
    # = getSession(url, headers)

    # while flag:
    #     time.sleep(3)
    # r = getRequest(url, headers, session)
    # print(r.status_code)
    # bsObj = BeautifulSoup(r.text, 'html.parser')
    # print(bsObj)
    #     aTags = bsObj.find_all("a", text="查看")
    #     for a in aTags:
    #         td = a.parent
    #         print(td)
    #         dateObj = td.find_previous_sibling("td")
    #         if dateObj is not None and dateObj.get_text() <= date:
    #             flag = False
    #             break
    #         urlList.append(a.attrs['href'])
    #     currentPage = currentPage + 1
    #     params["currentPage"] = currentPage
    #     print(params)
    # print(urlList)
    #
    # for aUrl in urlList[::-1]:
    #     id = id + 1
    #     data = []
    #     data.append(id)
    #     time.sleep(3)
    #     r = session.get(baseUrl + aUrl, headers=headers)
    #     print(r.status_code)
    #     bsObj = BeautifulSoup(r.text, 'html.parser')
    #     trs = bsObj.find("table", {"class": "detailview"}).find_all("tr")
    #     for tr in trs:
    #         if tr is None :
    #             continue
    #         tds = tr.find_all("td", width="75%")
    #         for td in tds:
    #             data.append(td.get_text().strip())
    #     print(tuple(data))
    #     print(len(tuple(data)))
    #

    #
    print(returnNumber)
finally:
    cursor.close()
    phoenix_conn.close()

# print(len(urlList))


# print('爬完了！')
### 一些可能用到的代码

# from selenium import webdriver
# driver = webdriver.Chrome(executable_path=r'D:\chromedriver_win32\chromedriver.exe')
# url="https://bbs.byr.cn/"
# driver.get(url)
# driver.implicitly_wait(1)
# print(driver.get_cookies())
# print(driver.page_source)

# savedCookies=r.cookies.get_dict()

# print(r.text)
# print('------------------------------')

# session = requests.Session()
# req = session.get(url, headers=headers)
# bsObj = BeautifulSoup(req.text)
# print(bsObj.find("table",{"class":"table-striped"}).get_text)
