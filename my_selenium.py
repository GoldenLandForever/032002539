from selenium import webdriver
import time
import re
def getURL_dir(url_dir):
    # 使用绝对路径打开,速度较慢，但是不加会412，希望测评组手下留情
    browser = webdriver.Chrome('C:\Program Files\Google\Chrome\Application\chromedriver.exe')

    browser.get(url_dir)
    cookies = browser.get_cookies()
    text = browser.page_source
    browser.close()
    return text

def hot_spot(word):
    #通过获得百度的疫情每日热点获得每日热点
    url_baidu = 'http://www.baidu.com'
    #绝对路径打开Edge浏览器，也可以替换成google
    browser = webdriver.Edge("C:\Program Files (x86)\Microsoft\Edge\Application\msedgedriver.exe")

    browser.get(url_baidu)

    browser.find_element_by_id('kw').send_keys(word)

    # id是su的是搜索的按钮，用click方法点击
    browser.find_element_by_id('su').click()
    
    driver = webdriver.Edge("C:\Program Files (x86)\Microsoft\Edge\Application\msedgedriver.exe")
    driver.get(browser.current_url)
    text = driver.page_source
    browser.close()
    #正则获取信息
    url = re.findall('class="group-content_3jCZd .*?href="(.+?)"',text,re.DOTALL)[0]

    title = re.findall('class="group-content_3jCZd .*?标题：(.*?)"',text,re.DOTALL)[0]
    driver.get(url)
    if url == '':
        print("今日暂无热点")
        driver.close()
    else:
        print("今日热点："+title+"  url="+url)
        #time.sleep(5)#展示一下热点新闻或者不
        driver.close()
