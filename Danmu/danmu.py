# 爬取B站视频弹幕-简单版本
# 方法：在视频的链接中的bilibili前，添加一个ibilibili，跳转到别人的接口
# 从这个接口中，可以看到弹幕的链接
url_danmu=r'https://api.bilibili.com/x/v1/dm/list.so?oid=1277596484'

# 接下来就可以从这个链接中获取数据了

# 观察这个链接，我们可以发现，这面又一串数字，叫oid，复制这个oid，到原视频的源代码中查看
# 可以看到，在源代码中是可以找到，因此
# 我们可以在源代码中解析得到oid，和弹幕接口进行拼接，然后获取不同视频的弹幕

# 在这之前，我们可以看一下oid在哪个位置，可以看到，在window——info中是有的
# 可以看到last_play_cid其实就是oid

import requests
import re
import json
import pprint

url=r'https://www.bilibili.com/video/BV1wu41137bg/'  #原视频的网址

header={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
    "Referer":"https://www.bilibili.com/",
}

resp=requests.get(url=url,headers=header)
# print(resp.text)
# ok 得到数据了
obj=re.compile(r'window.__playinfo__=(.*?)</script>',re.S)
html=obj.findall(resp.text)[0]
# print(html) #有输出，ok的
json_data=json.loads(html)
# pprint.pprint(json_data)
baseUrl=json_data['data']['dash']['video'][0]['baseUrl']
oid=baseUrl.split(r'/')[6] #在第七个
print(oid)

url_dan=f'https://api.bilibili.com/x/v1/dm/list.so?oid={oid}'

resp2=requests.get(url_dan,headers=header)

# 乱码了
resp2.encoding='utf-8'
# print(resp2.text)
# 不乱码了
obj2=re.compile(r'<d.*?>(.*?)</d')
# print(oid) 拿不到
# 算了挺难找的，直接从网址里面解析叭
danmus=obj2.findall(resp2.text)
print(danmus)
with open(r'danmu.txt',mode='w',encoding='utf-8') as f:
    for danmu in danmus:
        f.write(danmu+'\n')

print('爬取完成')
# 成功！