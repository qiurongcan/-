# 爬取用户的详细数据
# 第一步：从文件中获取mid和uid
# 第二步：得到mid和uid然后组成评论链接，获取用户uid，再访问用户

import requests
from lxml import etree
import re
import json
import pandas as pd

# 读取热搜文件
df=pd.read_excel(r'non_data2.xlsx')
# 遍历每一条热搜
for i in range(len(df.index)):
    uid=df['uid'][i]
    mid=df['mid'][i]

    base_url=r'https://weibo.com/ajax/statuses/buildComments?'

    # 组合网址
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



    header={
        "Cookie":"login_sid_t=885c922b9790ad7cd2a46845ee223644; cross_origin_proto=SSL; _s_tentry=cn.bing.com; UOR=cn.bing.com,weibo.com,cn.bing.com; Apache=6360589708598.268.1701169397544; SINAGLOBAL=6360589708598.268.1701169397544; ULV=1701169397546:1:1:1:6360589708598.268.1701169397544:; WBtopGlobal_register_version=2023112819; SUB=_2A25IYaatDeRhGeRJ6lcT-CbPyjyIHXVrHqZlrDV8PUNbmtANLUT8kW9NUt-V11WeIJxsbsrARMK6UR2vW8F10hbZ; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFPVmOC7sh7W5a3yBO3nRJz5JpX5KzhUgL.FozNeK-E1hn0eK52dJLoI7yWdG8QqPxGd7tt; ALF=1732708989; SSOLoginState=1701172989",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
    }

    idss=[]
    obj3=re.compile(r'"user":{"id":(.*?),',re.S)

    # 请求数据
    resp3=requests.get(url=base_url,headers=header,params=param)
    # print(resp3.text)
    # 使用re解析数据
    ids=obj3.findall(resp3.text)
    # print(ids)
    # print(len(ids))

    idss.extend(ids)
    json_data=json.loads(resp3.text)
    print(idss)

    # 获取下一页评论网址的id
    max_id=json_data['max_id']

    # 请求剩余页的评论
    while(int(max_id)!=0):
        # break
        next_param={
            'flow': 0,
            'is_reload': 1,
            'id': mid,
            'is_show_bulletin': 2,
            'is_mix': 0,
            'max_id': max_id,
            'count': 10,
            'uid': uid,
            'fetch_level': 0,
            'locale': 'zh',
        }
        # 请求数据
        resp4=requests.get(url=base_url,headers=header,params=next_param)
        # 解析数据
        ids=obj3.findall(resp4.text)
        # ids=ids.append()
        json_data=json.loads(resp4.text)
        # 继续得到下一页评论网址的id
        max_id=json_data['max_id']
        # print(ids)
        print(len(ids))
        idss.extend(ids)
        if len(ids)==0:
            break
        
    
    new_data={
        "uid":idss,
        "热搜":len(idss)*[df['热搜主题'][i]],
        "分类":len(idss)*[df['分类'][i]]

    }
    # 转化为DataFrame数据类型
    df2=pd.DataFrame(new_data)

    print(len(idss))
    # 保存数据
    df2.to_excel(f'每个热搜对应的用户信息/第{i}次.xlsx',index=None)

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