
import requests
import json
import os
import pandas as pd
from time import sleep

basePath=r'每个热搜对应的用户信息'

def get_detail(uid):

    base_url=f'https://weibo.com/ajax/profile/detail?uid={uid}'

    header={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
        # "Cookie":"UOR=,,login.sina.com.cn; SINAGLOBAL=9004892823532.627.1696855931093; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFPVmOC7sh7W5a3yBO3nRJz5JpX5KMhUgL.FozNeK-E1hn0eK52dJLoI7yWdG8QqPxGd7tt; ALF=1703945402; SSOLoginState=1701353402; SCF=AsBDKqChQ-5xm_eSXmMkhfwwFx9R2Md6CurhU06tAhv_8XUNCx4ST-PToVRFX5P8gmm_p3ya0VC-GQTpqKw1sQQ.; SUB=_2A25IbOfrDeRhGeRJ6lcT-CbPyjyIHXVrAGUjrDV8PUNbmtANLRXBkW9NUt-V1xjKYjQCeUc6gpEK6rp-TclYh106; _s_tentry=www.weibo.com; Apache=6527243363914.068.1701353551010; ULV=1701353551068:14:2:1:6527243363914.068.1701353551010:1699105959158",
        "Cookie":"UOR=,,login.sina.com.cn; SINAGLOBAL=9004892823532.627.1696855931093; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFPVmOC7sh7W5a3yBO3nRJz5JpX5KMhUgL.FozNeK-E1hn0eK52dJLoI7yWdG8QqPxGd7tt; ALF=1703945402; SSOLoginState=1701353402; SCF=AsBDKqChQ-5xm_eSXmMkhfwwFx9R2Md6CurhU06tAhv_8XUNCx4ST-PToVRFX5P8gmm_p3ya0VC-GQTpqKw1sQQ.; SUB=_2A25IbOfrDeRhGeRJ6lcT-CbPyjyIHXVrAGUjrDV8PUNbmtANLRXBkW9NUt-V1xjKYjQCeUc6gpEK6rp-TclYh106; _s_tentry=www.weibo.com; Apache=6527243363914.068.1701353551010; ULV=1701353551068:14:2:1:6527243363914.068.1701353551010:1699105959158; XSRF-TOKEN=ZnjZ0W4Hyg1pBn0OD6lKDRab; WBPSESS=Cso-iv5zxrwCpwu2e926RPAB6SqccHnPf_lUsAaM8eFRrant1Zny2P7Zljio065h_rUZxEh8vZdicXldORS4f-1ckefUcWJWw3rkOHqtRFYtPmfcfPHmtRBlaVJriAvj25m0TFtNPRd0vmY5CGklpw==",
    }

    resp=requests.get(url=base_url,headers=header)
        # print(resp.text)
    # 转化为json格式
    json_data=json.loads(resp.text)
    # print(resp.text)
    try:
        birthday=json_data['data']['birthday']
    except:
        birthday=None
    try:
        creat_at=json_data['data']['created_at']
    except:
        creat_at=None
    try:
        gender=json_data['data']['gender']
    except:
        gender=None
    try:
        location=json_data['data']['ip_location']
    except:
        location=None

    # 返回数据
    return birthday,creat_at,gender,location


dir1=os.listdir(r'每个热搜对应的用户信息')
dir2=os.listdir(r'完整版本')

dirs=list(set(dir1)^set(dir2))

# 读取目录下的文件
for dir in dirs:
    path=os.path.join(basePath,dir)
    # print(path)
    df=pd.read_excel(path)

    # 创建新的列并命名
    df['生日']=None
    df['性别']=None
    df['创建日期']=None
    df['IP']=None

    for i in range(len(df.index)):
        uid=int(df['uid'][i])
        try:
            # 请求数据
            birthday,creat_at,gender,location=get_detail(uid)
        except:
            print(f'第{i}个报错')
            continue
        # 存储数据
        df['生日'][i]=birthday
        df['性别'][i]=gender
        df['创建日期'][i]=creat_at
        df['IP'][i]=location
        print(f'完成{birthday}的爬去～')
        # break
    # 保存数据
    df.to_excel(r'完整版本/'+dir,index=None)
    print(f'完成{dir}的爬取～')
    sleep(1)

    # break



