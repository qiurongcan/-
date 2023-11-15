# 爬取B站视频--在网页源代码中
# 在网页源代码中将视频和音频链接拿到
# 访问后将视频音频保存并且合并到同一个视频文件中
# 得到完整的视频
import requests
import re
import json
import os
from pprint import pprint

url=r'https://www.bilibili.com/video/BV1pg4y1d77K/'

header={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.76",
    "Referer":"https://www.bilibili.com/",
}

resp=requests.get(url=url,headers=header)
# print(resp.text) #成功获取得到数据

obj=re.compile(r'window.__playinfo__=(.*?)</script>',re.S)

html_data=obj.findall(resp.text)[0]

json_data=json.loads(html_data) #是一个字典的形式
# pprint(json_data)  #格式化输出成功

base_data=json_data['data']
# 视频接受的码率 的 种类
accept_quality=base_data['accept_quality']
print(accept_quality) # 可以选择其中的一种进行爬取

videos=base_data['dash']['video'] #得到一个列表形式的字典

# for video in videos:
video=videos[0]['base_url']
audios=base_data['dash']['audio']
audio=audios[0]['baseUrl']
print(video)

video_data=requests.get(video,headers=header).content
with open("test.mp4",mode='wb') as f:
    f.write(video_data)

audio_data=requests.get(audio,headers=header).content
with open("test.mp3",mode='wb') as f:
    f.write(audio_data)


command=r'ffmpeg -i test.mp4 -i test.mp3 -acodec copy -vcodec copy test2.mp4'
os.system(command=command)



