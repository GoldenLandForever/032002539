import re
import my_Selenium
from pyecharts.globals import ThemeType
from pyecharts import options as opts
from pyecharts.charts import *
import pandas as pd
def City(city):
    #判断数据是否是需要统计的城市
    list = ['河北', '山西', '辽宁', '吉林', '黑龙江', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南', '湖北', '湖南', '广东', '海南',
                 '四川', '贵州', '云南', '陕西', '甘肃', '青海', '内蒙古', '广西', '西藏', '宁夏', '新疆', '北京', '天津', '上海', '重庆']

    return list.count(city)

def write2excel(data,cn1,cn2,name):
    #使用pandas导出excel
    write2exce = pd.DataFrame(data,index=list(range(1,len(data.keys())+1)),columns=[cn1,cn2])
    write2exce[cn1] = data.keys()
    write2exce[cn2] = data.values()
    write2exce.to_excel(name)

def my_Bar(data,name):
    bar = Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
    bar.add_xaxis(list(data.keys()))
    bar.add_yaxis("新增人数", list(map(int, data.values())), category_gap= '80%')
    bar.set_global_opts(
        title_opts=opts.TitleOpts(title=name),
        # 设置数据缩放滑块
        datazoom_opts=opts.DataZoomOpts(),
    )
    bar.render(name)


def my_main():
    # 获取url
    for cnt in range(1,40):
        if cnt == 1 :
            url_dir = "http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml"
        else:
            url_dir = 'http://www.nhc.gov.cn/xcs/yqtb/list_gzbd_'+str(cnt)+'.shtml'
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
            date_Get_year = re.findall('<span>发布时间.+?([0-9]{4})', contents_target, re.DOTALL)
            #获取全部段落
            content_target = re.findall('>(.*?)<', contents_target)
            text = ''
            for i in content_target:
                text += i
            ##正则筛选目标数据
            text_target = re.findall('新增确诊病例(.*?)例',text)[0]
            text_target_null = re.findall('新增无症状感染者(.*?)例',text)[0]
            data_nation = {}
            data_nation['新增确诊病例'] = text_target
            data_nation['新增无症状感染者'] = text_target_null


            #正则筛选目标数据
            city_newcases = re.findall('本土病例.*?(.*?)）',text)[0]
            city_newcases_key = re.findall('([\u4E00-\u9FA5]+?)[0-9]*?例',city_newcases)
            city_newcases_value = re.findall('[\u4E00-\u9FA5]+?([0-9]*?)例',city_newcases)

            data_newcases = {}
            # 判断是否在统计城市
            for i  in range(0,len(city_newcases_key)):
                if City(city_newcases_key[i]) == 1 :
                    data_newcases[city_newcases_key[i]] = city_newcases_value[i]

            # 正则筛选目标数据
            data_null = {}
            city_null = re.findall('本土[0-9]*?例（(.*?)）',text)[0]
            city_null_key = re.findall('([\u4E00-\u9FA5]+?)[0-9]*?例',city_null)
            city_null_value = re.findall('[\u4E00-\u9FA5]+?([0-9]*?)例',city_null)
            #判断是否在统计城市
            for i  in range(0,len(city_null_key)):
                if City(city_null_key[i]) == 1 :
                    data_null[city_null_key[i]] = city_null_value[i]

            #导出execel表格
            write2excel(data=data_nation, cn1='新增类型', cn2='新增数量', name='中国大陆'+date_Get_year[0]+'年' + date_Get[0] + '疫情通报.xlsx')
            write2excel(data_newcases,'省份','新增确诊','各省份'+date_Get_year[0]+'年' + date_Get[0] + '新增确诊疫情通报.xlsx')
            write2excel(data_null,'省份','无症状感染者','各省份'+date_Get_year[0]+'年' + date_Get[0] + '无症状感染者疫情通报.xlsx')
            #数据可视化
            my_Bar(data_nation,'中国大陆'+date_Get_year[0]+'年'+date_Get[0]+'疫情柱状图.html')
            my_Bar(data_newcases,'各省份'+date_Get_year[0]+'年'+date_Get[0]+'新增确诊柱状图.html')
            my_Bar(data_null,'各省份'+date_Get_year[0]+'年'+date_Get[0]+'新增无症状柱状图.html')


if __name__ == '__main__':
    my_main()
