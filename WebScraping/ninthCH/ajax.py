from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import StaleElementReferenceException
def waitForLoad(driver):
    elem = driver.find_element_by_tag_name("html")
    count = 0
    while True:
        count += 1
        if count > 20:
            print("Timing out after 10 seconds and returning")
            return
        time.sleep(.5)
    try:
        elem == driver.find_element_by_tag_name("html")
    except StaleElementReferenceException:
        return
driver = webdriver.Chrome(executable_path=r'D:\chromedriver_win32\chromedriver.exe')
driver.get("http://pythonscraping.com/pages/javascript/redirectDemo1.html")
waitForLoad(driver)
print(driver.page_source)

# 隐式等待
# from selenium.webdriver.support import expected_conditions as EC
# driver = webdriver.Chrome(executable_path=r'D:\chromedriver_win32\chromedriver.exe')
# driver.get("http://pythonscraping.com/pages/javascript/ajaxDemo.html")
# try:
#     element = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.ID, "loadedButton")))
# finally:
#     print(driver.find_element_by_id("content").text)
#     driver.close()


# 显式等待
# driver = webdriver.Chrome(executable_path=r'D:\chromedriver_win32\chromedriver.exe')
# driver.get("http://pythonscraping.com/pages/javascript/ajaxDemo.html")
# time.sleep(3)
# print(driver.find_element_by_id('content').text)
# driver.close()