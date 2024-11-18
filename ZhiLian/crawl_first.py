# pip install python-box
import requests
from box import Box
import json
from lxml import etree
import pandas as pd



# 需要抓取数据的八个城市
target_city = ['北京', '上海', '广州', '长春', '天津', '重庆', '西安', '杭州']

with open(r'hotcity.json', encoding='utf-8') as f:
    json_datas = json.loads(f.read())

target_code = []
for data in json_datas:
    city_data = Box(data)
    # 读取城市编码
    if city_data.name in target_city:
        print(city_data.name, ", code:", city_data.code)
        target_code.append(city_data.code)

# print(target_code)
target_code = ['530', '538', '763', '531', '854', '613', '653', '551']






url = r'https://www.zhaopin.com/'

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
}

resp = requests.get(url=url, headers=headers)
# print(resp.text)

# https://www.zhaopin.com/sou/jl530/kw01500O80EO062NO0AF8G/p2

# 解析页面
html_data = etree.HTML(resp.text)
categories = html_data.xpath('//*[@id="root"]/main/div[1]/div[1]/ol/li')

f_writer = pd.ExcelWriter(r'智联八个类别专业分类以及每个类别职业信息.xlsx')

# 一共是9类，最后一类不考虑
for category_li in categories[:8]:
    divs = category_li.xpath(r'./nav/div')
    cls_name = divs[0].xpath(r'./h4/text()')[0]
    # 替换斜杠
    cls_name = cls_name.replace("/",'-')
    # print(cls_name)
    career = []
    href = []
    # 创建空数据
    df = pd.DataFrame()
    for div in divs:
        a = div.xpath(r'./div/a')
        # print(a)
        for detail in a:
            c_ = detail.xpath(r'./text()')[0]
            # print(c_)
            h_ = detail.xpath(r'./@href')[0]
            career.append(c_)
            href.append(h_)
    
    df['职业二级分类'] = career
    df['Base_url'] = href

    df.to_excel(f_writer, sheet_name=cls_name, index=False)

        # result = div.xpath(r'./div/a/text()')
        # releated_url = div.xpath(r'./div/a/@href')
        # print(result)
        # print(releated_url)

f_writer.close()