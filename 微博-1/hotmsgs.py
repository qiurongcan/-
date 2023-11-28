# 首先，爬取微博热搜 20000条热搜

import requests
import json
import pandas as pd

# 打开存储数据的文件夹
data=pd.read_excel(r'data1.xlsx')

# i=len(data.index)
# print(i)
print(type(data))


# 微博热搜网址
url='https://weibo.com/ajax/side/hotSearch'

header={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
}

resp=requests.get(url=url,headers=header)
print(resp.text) #得到数据，然后进行json解析

# 转换为json格式的数据
json_data=json.loads(resp.text) 

# 解析数据 -> 得到一个热搜列表
realtime_list=json_data['data']['realtime']
print((realtime_list[0]['category']))
# 对单一的项目进行数据提取
for realtime in realtime_list:
    category=realtime['category']
    note=realtime['note']
    word_scheme=realtime['word_scheme']
    word=realtime['word']
    raw_hot=realtime['raw_hot']
    detail_web=f'https://s.weibo.com/weibo?q=%23{note}%23'
    new_data={
        '热搜主题':note,
        '分类':category,
        '关键词':word,
        '词话':word_scheme,
        '热度':raw_hot,
        '是否采集':0,
        '详细网址':detail_web
        }
    # data['热搜主题'][i]=note
    # data['分类'][i]=category
    # data['关键词'][i]=word
    # data['词话'][i]=word_scheme
    # data['热度'][i]=raw_hot
    # data['是否采集'][i]=0
    data=data._append(new_data,ignore_index=True)


data.to_excel('data1.xlsx',index=None)
print("------------爬取完成-----------")





