import re
import my_Selenium
import my_homework

def other_regions():
    data_HK = -1
    data_AM = -1
    data_TW = -1
    date_Get_early = ''
    for cnt in range(1, 40):
        if cnt == 1:
            url_dir = "http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml"
        else:
            url_dir = 'http://www.nhc.gov.cn/xcs/yqtb/list_gzbd_' + str(cnt) + '.shtml'
        # 正则筛url
        contents_directory = my_Selenium.getURL_dir(url_dir)
        contents_directory = re.findall('<ul class="zxxx_list">.*?</ul>', contents_directory, re.DOTALL)
        content_directory = re.findall('href="(.*?)" target', contents_directory[0], re.DOTALL)
        i = 0
        for url_target_half in content_directory:

            url_target = "http://www.nhc.gov.cn" + url_target_half  # 生成目标URL
            # 打开网页
            contents_target = my_Selenium.getURL_dir(url_target)
            # 获取时间
            date_Get = re.findall('<div class="tit">截至(.*?)24时', contents_target)
            date_Get_year = re.findall('<span>发布时间.+?([0-9]{4})',contents_target,re.DOTALL)
            # 获取全部段落
            content_target = re.findall('>(.*?)<', contents_target)
            text = ''
            for i in content_target:
                text += i
            ##正则筛选目标数据
            data_newcases = {}
            # 港澳台数据
            other_newcases = re.findall('港澳台地区通报(.*?)）。', text)[0]
            if data_HK != -1:
                data_newcases['香港特别行政区'] = data_HK - int(re.findall('香港特别行政区([0-9]+?)例', other_newcases)[0])
                data_newcases['澳门特别行政区'] = data_AM - int(re.findall('澳门特别行政区([0-9]+?)例', other_newcases)[0])
                data_newcases['台湾地区'] =data_TW - int(re.findall('台湾地区([0-9]+?)例', other_newcases)[0])
                data_HK = int(re.findall('香港特别行政区([0-9]+?)例', other_newcases)[0])
                data_AM = int(re.findall('澳门特别行政区([0-9]+?)例', other_newcases)[0])
                data_TW = int(re.findall('台湾地区([0-9]+?)例', other_newcases)[0])
            else:
                data_HK = int(re.findall('香港特别行政区([0-9]+?)例', other_newcases)[0])
                data_AM = int(re.findall('澳门特别行政区([0-9]+?)例', other_newcases)[0])
                data_TW = int(re.findall('台湾地区([0-9]+?)例', other_newcases)[0])

            # 导出execel表格
            if date_Get_early == '':
                date_Get_early = date_Get[0]
            else:
                my_homework.write2excel(data_newcases,'省份','新增确诊','港澳台地区'+date_Get_year[0]+'年' + date_Get_early + '新增确诊疫情通报.xlsx')
            # 数据可视化
                my_homework.my_Bar(data_newcases, '港澳台地区' +date_Get_year[0]+'年'+date_Get_early + '新增确诊柱状图.html')
                date_Get_early = date_Get[0]
        break

if __name__ == '__main__':
    other_regions()
