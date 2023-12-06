import re
import time
import requests
import urllib
import json
from urllib import parse
from hashlib import md5

# 从源网页获取oid
origin_url='https://www.bilibili.com/video/BV1Gc411D7ni/'
# 请求头
header1={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
}

# 正则匹配
obj=re.compile(r'"cidMap":{"(.*?)":{',re.S)
resp1=requests.get(url=origin_url,headers=header1)
# 获取评论的oid
oid=obj.findall(resp1.text)[0]
resp1.close()
# print(resp1.text)


# ------------------定值--------------------- #
ct="ea1db124af3c7062474693fa704f4ff8"

header2={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
    "Cookie":"buvid3=87AB7053-858C-6093-B4CF-4A3CD150773376912infoc; b_nut=1695788176; i-wanna-go-back=-1; b_ut=7; _uuid=4A989FC6-FFDF-B15D-1EFA-77EF610BAEB9F75574infoc; buvid_fp=a1709f14cbd2b8a5c1fef5b37aab8ea2; buvid4=8743E9DB-5F18-800A-7E83-8359CA1BF4D677562-023092712-PdJr0jKE6N5pSQNdyTYMzr8F2IhY9DzV; home_feed_column=5; CURRENT_FNVAL=4048; rpdid=0z9Zw2XHhL|NXO5GbV6|gz|3w1QLlYS; DedeUserID=476956332; DedeUserID__ckMd5=8bb8ec02cf438f22; hit-dyn-v2=1; enable_web_push=DISABLE; header_theme_version=CLOSE; LIVE_BUVID=AUTO1616989118604773; bp_video_offset_476956332=866271891190448181; PVID=1; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDIwMTM1NzEsImlhdCI6MTcwMTc1NDMxMSwicGx0IjotMX0.aD__KJ-pV9WBQCt-wekR6eZA-4H57XqqcmRHuRysqms; bili_ticket_expires=1702013511; SESSDATA=97586540%2C1717306372%2C74114%2Ac1CjBsSFaCHhPrjxmOj2MCE6WCS9H5hO3mzl7edFjwXxbIQNJXUNDwv9SV6_GziyWckl4SVjI3UjlJbkhhYnpXNDVYajVvbjF2YklzNVJYdUVRMUFNbVNjZUdfMks1VUduSE0xb2hGRm9QYlAweGRJVERub3ZHQmNvcW14ZEhaMEpqVU5GdzlEWTlRIIEC; bili_jct=50ae985be86cba663bdf669a8e12452c; sid=4xea3k1c; fingerprint=9d56312efc56e939901cacbfe8ab854a; b_lsid=894108A87_18C3D498EF3; bsource=search_bing; browser_resolution=1872-966",
}

# ------------------请求第一页的----------------------#
# --获取wts
wts=int(time.time())
# 第一页和剩下页的有不一样
# --获取pagination_str1
pagination_str1='{"offset":""}'
# 进行url编码
pagination_str1=urllib.parse.quote(pagination_str1)

# --------解析w_rid-------#
Ut1=f"""mode=3&oid={oid}&pagination_str={pagination_str1}&plat=1&seek_rpid=&type=1&web_location=1315875&wts={wts}"""
# md5加密
w_rid=md5((Ut1+ct).encode()).hexdigest()
base_url=f'https://api.bilibili.com/x/v2/reply/wbi/main?oid={oid}&type=1&mode=3&pagination_str={pagination_str1}&plat=1&seek_rpid=&web_location=1315875&w_rid={w_rid}&wts={wts}'

resp2=requests.get(url=base_url,headers=header2)
# print(resp2.text)

# 从第一页获取session_id
json_data1=json.loads(resp2.text)
# 需要加上cookie才能得到seesion_id
session_id=json_data1['data']['cursor']['session_id']
# print(session_id)

reply=json_data1['data']['replies'][1]['content']['message']
print(reply)

# ----------------------------解析第二页和其他页--------------------------#

def req_other():

    wts2=int(time.time())
    # --获取pagination_str2
    pagination_str2='{"offset":"{\"type\":1,\"direction\":1,\"session_id\":\"'+session_id+'\",\"data\":{}}"}'

    # 进行url编码
    pagination_str2=urllib.parse.quote(pagination_str2)

    # --------解析w_rid-------#
    Ut2=f'mode=3&oid={oid}&pagination_str={pagination_str2}&plat=1&type=1&web_location=1315875&wts={wts2}'
    # md5加密
    w_rid2=md5((Ut2+ct).encode()).hexdigest()

    base_url2=f'https://api.bilibili.com/x/v2/reply/wbi/main?oid={oid}&type=1&mode=3&pagination_str={pagination_str2}&plat=1&web_location=1315875&w_rid={w_rid2}&wts={wts2}'
        
    resp=requests.get(url=base_url2,headers=header2)
    print(resp.text)
    # json_data2=json.loads(resp.text)
    # reply1=json_data2['data']['replies'][0]['content']['message']
    # print(reply1)

time.sleep(1)

req_other()

