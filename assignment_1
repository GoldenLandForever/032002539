import re
import time
import requests
from openpyxl.workbook import Workbook
import pandas as pd
from pandas import Series

#定义url
url_dir = "http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml"
#获取cookie
rs = requests.get(url_dir)
cookie = ""
for k, v in rs.cookies.items():
    cookie += k + '=' + v + ';'

#定义请求头
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27"
}
headers["Cookie"] = cookie
#发送请求，获取响应
response = requests.get(url_dir,headers=headers)

#解码
response.raise_for_status()
response.encoding = response.apparent_encoding
contents_directory = response.text

content_directory = re.findall('href="(.*?)" target',contents_directory,re.DOTALL)
i = 0
for url_target_half in content_directory:
    url_target = "http://www.nhc.gov.cn" + url_target_half#生成目标URL
    res = requests.get(url_target,headers=headers)
    #res.raise_for_status()
    res.encoding = res.apparent_encoding
    contents_target = res.text

    #获取时间
    date_Get = re.findall('<div class="tit">截至(.*?)24时',contents_target)
    content_target = re.findall('<p style="text-align: justify;.*?</p>',contents_target,re.DOTALL)

    data = {}

    if not content_target:
        continue
    if date_Get[0] > '8月30日':
        newCases = re.findall('新增确诊病例.*?16pt;">(.*?)</span>',content_target[0],re.DOTALL)[0]
        newCases_null = re.findall('新增无症状感染者.*?16pt;">(.*?)</span>', content_target[4], re.DOTALL)[0]
        data["新增确诊"] = newCases
        data["新增无症状感染者"] = newCases_null
    else:
        newCases = re.findall('新增确诊病例(.*?)例',content_target[0])[0]
        newCases_null = re.findall('新增无症状感染者(.*?)例', content_target[4])[0]
        data["新增确诊"] = newCases
        data["新增无症状感染者"] = newCases_null

    write2excel = pd.DataFrame(data,columns=['新增类型','新增人数'],dtype=float)
    data_key = list(data.keys())
    data_value = list(data.values())
    write2excel['新增类型'] = data_key
    write2excel['新增人数'] = data_value
    write2excel.to_excel('中国大陆'+date_Get[0]+'疫情通报.xlsx')
    i += 1
    if i == 7 :
        break#先爬7天的
