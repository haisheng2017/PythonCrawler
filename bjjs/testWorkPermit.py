import requests
import re
import phoenixdb
import phoenixdb.cursor
import time
from bs4 import BeautifulSoup

headers = {
    "User-Agent": r"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36",
    "Accept": r"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Host": r"www.bjjs.gov.cn",
    "Origin": r"http://www.bjjs.gov.cn",
    "Referer": r"http://www.bjjs.gov.cn/eportal/ui?pageId=308891"
}

url = r"http://www.bjjs.gov.cn/eportal/ui?pageId=308891"
baseUrl = r"http://www.bjjs.gov.cn"


def getSession(loginUrl, headers, params):
    if loginUrl is not None:
        session = requests.Session()
        r = session.post(loginUrl, data=params, headers=headers)
        print(r.status_code)
        return session


def getRequest(url, headers, params, session):
    if url is not None:
        r = session.post(url, data=params, headers=headers)

        return r


currentPage = 1
params = {
    "filter_LIKE_GCMC": "",
    "filter_LIKE_SGXKZH": "",
    "filter_LIKE_JSDW": "",
    "filter_LIKE_SGDW": "",
    "filter_LIKE_JLDW": "",
    "filter_LIKE_SJDW": "",
    "currentPage": currentPage,
    "pageSize": 15,
    "OrderByField": "",
    "OrderByDesc": ""
}

database_url = 'http://node1:8765/'
phoenix_conn = phoenixdb.connect(database_url, autocommit=True)
cursor = phoenix_conn.cursor(cursor_factory=phoenixdb.cursor.DictCursor)
try:

    cursor.execute(
        "SELECT * FROM THIRDWORK_PERMIT ORDER BY case when PERMITDATE is null then 1 else 0 end asc ,PERMITDATE desc limit 1")
    date = cursor.fetchone()['PERMITDATE'].strftime('%Y-%m-%d')
    cursor.execute("SELECT * FROM THIRDWORK_PERMIT ORDER BY id desc limit 1")
    id = cursor.fetchone()['ID']

    flag = True
    session = getSession(url, headers, params)
    urlList = []
    while flag:
        time.sleep(3)
        r = getRequest(url, headers, params, session)
        print(r.status_code)
        bsObj = BeautifulSoup(r.text, 'html.parser')
        # print(bsObj)
        aTags = bsObj.find_all("a", text="查看")
        for a in aTags:
            td = a.parent
            print(td)
            dateObj = td.find_previous_sibling("td")
            if dateObj is not None and dateObj.get_text() <= date:
                flag = False
                break
            urlList.append(a.attrs['href'])
        currentPage = currentPage + 1
        params["currentPage"] = currentPage
        print(params)
    print(urlList)

    for aUrl in urlList[::-1]:
        id = id + 1
        data = []
        data.append(id)
        time.sleep(3)
        r = session.get(baseUrl + aUrl, headers=headers)
        print(r.status_code)
        bsObj = BeautifulSoup(r.text, 'html.parser')
        trs = bsObj.find("table", {"class": "detailview"}).find_all("tr")
        for tr in trs:
            if tr is None :
                continue
            tds = tr.find_all("td", width="75%")
            for td in tds:
                data.append(td.get_text().strip())
        print(tuple(data))
        print(len(tuple(data)))

        cursor.execute("UPSERT INTO THIRDWORK_PERMIT(ID,PROJECTNAME,PERMITNUM,DISTRICT,BUILDER,SCALE,PERMITDATE,ADDRESS,CONSTRUCTIONUNIT,SUPERVISEUNIT,DESIGNUNIT,ADMINISTRATIONCODE,REPRESENTATIVENAME,PERMITUNIT,PERMITDEADLINE,CERTIFICATESTATUS) VALUES (?, ?, ?, ?,?, ?, TO_DATE(?,'yyyy-MM-dd'), ?, ?, ?, ?, ?, ?, ?, ?, ?)", tuple(data))


finally:
    cursor.close()
    phoenix_conn.close()

# print(len(urlList))


print('爬完了！')
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
