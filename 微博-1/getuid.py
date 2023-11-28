# 爬取用户的详细数据
# 第一步：从data1.xlsx详细网址中进入
# 第二步：获取评论相关的信息，得到mid和uid
# 第三步：得到mid和uid然后组成评论链接，获取用户uid，再访问用户

import requests
from lxml import etree
import re


url="https://s.weibo.com/weibo?q=%23%E5%BF%AB%E4%B9%90%E8%80%81%E5%8F%8B%E8%AE%B0%23"


header={
    "Cookie":"login_sid_t=885c922b9790ad7cd2a46845ee223644; cross_origin_proto=SSL; _s_tentry=cn.bing.com; UOR=cn.bing.com,weibo.com,cn.bing.com; Apache=6360589708598.268.1701169397544; SINAGLOBAL=6360589708598.268.1701169397544; ULV=1701169397546:1:1:1:6360589708598.268.1701169397544:; WBtopGlobal_register_version=2023112819; SUB=_2A25IYaatDeRhGeRJ6lcT-CbPyjyIHXVrHqZlrDV8PUNbmtANLUT8kW9NUt-V11WeIJxsbsrARMK6UR2vW8F10hbZ; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFPVmOC7sh7W5a3yBO3nRJz5JpX5KzhUgL.FozNeK-E1hn0eK52dJLoI7yWdG8QqPxGd7tt; ALF=1732708989; SSOLoginState=1701172989",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
}

resp=requests.get(url=url,headers=header)

# print(resp.text)
html_data=etree.HTML(resp.text)

obj1=re.compile(r'mid=(.*?)&',re.S)
obj2=re.compile(r'touid=(.*?)&',re.S)

urll=html_data.xpath(r'//*[@id="pl_feedlist_index"]/div[4]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/ul/li[1]/a/@onclick')[0]

mid=obj1.findall(urll)[0]
uid=obj2.findall(urll)[0]
# print(mid,uid)

param={
    'is_reload': 1,
    'id': mid,
    'is_show_bulletin': 2,
    'is_mix': 0,
    'count': 10,
    'uid': uid,
    'fetch_level': 0,
    'locale': 'zh',
}

base_url=r'https://weibo.com/ajax/statuses/buildComments?'

obj3=re.compile(r'"user":{"id":(.*?),',re.S)

resp3=requests.get(url=base_url,headers=header,params=param)
print(resp3.text)
ids=obj3.findall(resp3.text)
print(ids)
print(len(ids))
"""
is_reload: 1
id: 4969403905212601
is_show_bulletin: 2
is_mix: 0
count: 10
uid: 3196372733
fetch_level: 0
locale: zh
"""

"""
flow: 0
is_reload: 1
id: 4969403905212601
is_show_bulletin: 2
is_mix: 0
max_id: 143544826876819
count: 20
uid: 3196372733
fetch_level: 0
locale: zh
"""

"""
https://weibo.com/3196372733/Nt7vMlS2d

/html/body/div[1]/div[2]/div/div[2]/div[1]/div[4]/div[1]/div[2]/div[1]/div[2]/div[2]/a[1]/@href
"""