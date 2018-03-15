import requests
import json
import re
from bs4 import BeautifulSoup


def getSession(loginUrl,headers,params):
    if loginUrl is not None:
        session = requests.Session()
        r = session.post(loginUrl, data=params,headers=headers)
        return session
def findKeywords(keywords,content):
    for keyword in keywords:
        if content.find(keyword)!=-1:
            return 0
    return -1

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
           "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
           'x-requested-with':'XMLHttpRequest'}

#可以写成文件的形式存放帐号密码等

with open('user.json', 'r', encoding='utf-8') as user:
    params=json.loads(user.read())

print(params)



loginUrl="https://bbs.byr.cn/user/ajax_login.json"


session=getSession(loginUrl,headers,params)
#可以写循环，爬到不想爬

typeUrl="https://bbs.byr.cn/board/Job?p="
pageNum=1
keywords=("面经","经历")
urlList=[]
r=session.get(typeUrl+str(pageNum),headers=headers).text
bsObj = BeautifulSoup(r,'html.parser')
tbody=bsObj.find("table",{"class":"board-list tiz"}).find("tbody")
trs=tbody.findAll("tr")

for tr in trs:
    a=tr.find("td",{"class":re.compile("title_9.*")}).find('a')
    if findKeywords(keywords,a.get_text())!=-1:
        urlList.append(a.attrs["href"])
print(urlList)

for url in urlList:
    r=session.get('https://bbs.byr.cn'+url,headers=headers).text
    soup= BeautifulSoup(r,'html.parser')
    div=soup.find('div',{'class':'b-content corner'}).find('a',{'name':'a0'}).next_sibling.find('div',{'class':'a-content-wrap'})
    contentList=div.contents

    fileName=r'experiment/'+url.replace(r"/","_")
    suffix='.txt'
    with open(fileName+suffix, 'w', encoding='utf-8') as file:
        for content in contentList:
            if content.name is None:
                file.write(content)
            elif content.name.find('br')!=-1:
                file.write('\r\n')

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
