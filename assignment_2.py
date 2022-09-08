import re
import time
import requests
from openpyxl.workbook import Workbook
import pandas as pd
from pandas import Series
import  assignment_1


content_directory, headers = assignment_1.getUrl_dir()
i = 0

for url_target_half in content_directory:
    url_target = "http://www.nhc.gov.cn" + url_target_half  # 生成目标URL
    res = requests.get(url_target, headers=headers)
    # res.raise_for_status()
    res.encoding = res.apparent_encoding
    contents_target = res.text


    date_Get = re.findall('<div class="tit">截至(.*?)24时', contents_target)
    content_target = re.findall('<p style="text-align: justify;.*?</p>', contents_target, re.DOTALL)
    if not content_target:
        continue
    data1 = {}
    data2 = {}
    cnt1 = 0
    cnt2 = 0

    if date_Get[0] > '8月30日':
        newCases = re.findall('本土病例.*?（(.*?)）',content_target[0],re.DOTALL)[0]
        newCases_key = re.findall('([\u4E00-\u9FA5]+)<span style="font-fam',newCases)
        newCases_value = re.findall('<span style="font-family: 仿宋,仿宋_GB2312; font-size: 16pt;">(.*?)</span>',newCases)

        newCases_null = re.findall('本土(.*?)</p>',content_target[4],re.DOTALL)[0]
        newCases_null_key = re.findall('([\u4E00-\u9FA5]+)<span style="font-fam',newCases_null)
        newCases_null_value = re.findall('/span>.*?<span style="font-family: 仿宋,仿宋_GB2312; font-size: 16pt;">(.*?)<',newCases_null)

        for k in newCases_key:
            data1[k] = newCases_value[cnt1]
            cnt1 += 1
        for k in newCases_null_key:
            data2[k] = newCases_null_value[cnt2]
            cnt2 += 1

    else:
        newCases = re.findall('本土病例.*?（(.*?)）', content_target[0], re.DOTALL)[0]
        newCases_key = re.findall('([\u4E00-\u9FA5]+?)[0-9]*?例',newCases)
        newCases_value = re.findall('[\u4E00-\u9FA5]+?([0-9]*?)例',newCases)

        newCases_null = re.findall('本土.*?（(.*?)）',content_target[4],re.DOTALL)[0]
        newCases_null_key = re.findall('([\u4E00-\u9FA5]+?)[0-9]*?例',newCases_null)
        newCases_null_value = re.findall('[\u4E00-\u9FA5]+?([0-9]*?)例',newCases_null)
        for k in newCases_key:
            data1[k] = newCases_value[cnt1]
            cnt1 += 1
        for k in newCases_null_key:
            data2[k] = newCases_null_value[cnt2]
            cnt2 += 1

    write2excel_new = pd.DataFrame(data1, columns=['省份', '新增确诊'])
    write2excel_new['省份'] = data1.keys()
    write2excel_new['新增确诊'] = data1.values()
    write2excel_new.to_excel('各省份' + date_Get[0] +'新增确诊疫情通报.xlsx')

    write2excel_null = pd.DataFrame(data2,columns=['省份', '无症状感染者'])
    write2excel_null['省份'] = data2.keys()
    write2excel_null['无症状感染者'] = data2.values()
    write2excel_null.to_excel('各省份' + date_Get[0] +'无症状感染者疫情通报.xlsx')
    break
