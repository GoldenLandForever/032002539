import re
import time
import pyecharts
from pyecharts.charts import Bar
import my_Selenium
import pandas as pd

def assignment_1():
    # 获取url
    url_dir = "http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml"

    #正则筛url
    contents_directory = my_Selenium.getURL_dir(url_dir)
    contents_directory = re.findall('<ul class="zxxx_list">.*?</ul>',contents_directory,re.DOTALL)
    content_directory = re.findall('href="(.*?)" target', contents_directory[0], re.DOTALL)
    i = 0
    for url_target_half in content_directory:
        url_target = "http://www.nhc.gov.cn" + url_target_half  # 生成目标URL
        #打开网页
        contents_target = my_Selenium.getURL_dir(url_target)
        # 获取时间
        date_Get = re.findall('<div class="tit">截至(.*?)24时', contents_target)
        #获取全部段落
        content_target = re.findall('<p style="text-align: justify;.*?</p>', contents_target, re.DOTALL)

        data = {}

        if not content_target:
            continue
        #分时间正则
        if date_Get[0] > '8月30日':
            #从目标段落找关键词
            newCases = re.findall('新增确诊病例.*?16pt;">(.*?)</span>', content_target[0], re.DOTALL)[0]
            newCases_null = re.findall('新增无症状感染者.*?16pt;">(.*?)</span>', content_target[4], re.DOTALL)[0]
            data["新增确诊"] = newCases
            data["新增无症状感染者"] = newCases_null
        else:
            newCases = re.findall('新增确诊病例(.*?)例', content_target[0])[0]
            newCases_null = re.findall('新增无症状感染者(.*?)例', content_target[4])[0]
            data["新增确诊"] = newCases
            data["新增无症状感染者"] = newCases_null

        write2excel = pd.DataFrame(data, columns=['新增类型', '新增人数'], dtype=float)
        data_key = list(data.keys())
        data_value = list(data.values())
        write2excel['新增类型'] = data_key
        write2excel['新增人数'] = data_value
        write2excel.to_excel('中国大陆' + date_Get[0] + '疫情通报.xlsx')
        i += 1
        if i == 7:
            break
