# 首先，爬取微博热搜 20000条热搜

import requests
import json
import pandas as pd
import re
from lxml import etree
from time import sleep

# 打开存储数据的文件夹
data=pd.read_excel(r'data2.xlsx')

# i=len(data.index)
# print(i)


# 微博热搜网址
url='https://weibo.com/ajax/side/hotSearch'

header={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
}

header2={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
    "Cookie":"UOR=,,login.sina.com.cn; SINAGLOBAL=9004892823532.627.1696855931093; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFPVmOC7sh7W5a3yBO3nRJz5JpX5KMhUgL.FozNeK-E1hn0eK52dJLoI7yWdG8QqPxGd7tt; ALF=1703945402; SSOLoginState=1701353402; SCF=AsBDKqChQ-5xm_eSXmMkhfwwFx9R2Md6CurhU06tAhv_8XUNCx4ST-PToVRFX5P8gmm_p3ya0VC-GQTpqKw1sQQ.; SUB=_2A25IbOfrDeRhGeRJ6lcT-CbPyjyIHXVrAGUjrDV8PUNbmtANLRXBkW9NUt-V1xjKYjQCeUc6gpEK6rp-TclYh106; _s_tentry=www.weibo.com; Apache=6527243363914.068.1701353551010; ULV=1701353551068:14:2:1:6527243363914.068.1701353551010:1699105959158",
}

# 请求数据
resp=requests.get(url=url,headers=header)
# print(resp.text) #得到数据，然后进行json解析

# 转换为json格式的数据
json_data=json.loads(resp.text) 

# 解析数据 -> 得到一个热搜列表
realtime_list=json_data['data']['realtime']
# print((realtime_list[0]['category']))
# 对单一的项目进行数据提取
for realtime in realtime_list:
    try:
        category=realtime['category']
    except:
        category=None
    note=realtime['note']
    try:
        word_scheme=realtime['word_scheme']
    except:
        word_scheme=None
    word=realtime['word']
    try:
        raw_hot=realtime['raw_hot']
    except:
        raw_hot=None
    detail_web=f'https://s.weibo.com/weibo?q=%23{note}%23'

    # -------------------------------
    # 在这里还需要补充采集mid和uid，为下一步做准备
    resp2=requests.get(url=detail_web,headers=header2)

    obj3=re.compile(r'\?mid=(.*?)&touid=(.*?)&from.*?帮上头条',re.S)
    result=obj3.findall(resp2.text)[0]
    mid=result[0]
    uid=result[1]

    # sleep(0.1)
    print(f"完成{mid}的采集～")
    resp2.close()

    new_data={
        '热搜主题':note,
        '分类':category,
        '关键词':word,
        '词话':word_scheme,
        '热度':raw_hot,
        '是否采集':0,
        '详细网址':detail_web,
        'mid':mid,
        'uid':uid,
        }
    
    # 存储数据
    data=data._append(new_data,ignore_index=True)


resp.close()
# 保存文件
data.to_excel('data2.xlsx',index=None)
print("------------爬取完成-----------")





