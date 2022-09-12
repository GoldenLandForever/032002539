from selenium import webdriver

def getURL_dir(url_dir):
    browser = webdriver.Chrome('C:\Program Files\Google\Chrome\Application\chromedriver.exe')  # 使用绝对路径打开
    #使用selenium来模拟打开浏览器，速度较慢，但不会412
    browser.get(url_dir)
    cookies = browser.get_cookies()
    text = browser.page_source
    browser.close()
    return text

