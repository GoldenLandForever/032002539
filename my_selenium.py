from selenium import webdriver

def getURL_dir(url_dir):
    browser = webdriver.Chrome('C:\Program Files\Google\Chrome\Application\chromedriver.exe')  # 使用绝对路径打开

    browser.get(url_dir)
    cookies = browser.get_cookies()
    text = browser.page_source
    browser.close()
    return text

