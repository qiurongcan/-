# 爬取B站视频的评论，涉及js逆向
# 首先进行网站分析


# 可以看到，网址是在这个链接中的
# https://api.bilibili.com/x/v2/reply/wbi/main?oid=366804595&type=1&mode=3&pagination_str=%7B%22offset%22:%22%22%7D&plat=1&seek_rpid=&web_location=1315875&w_rid=0e7cc919fa550533aeb691fde2680b63&wts=1701779976

# 因此，只需要得到这个网址的链接即可

# 可以看到，会不断的加载评论的链接
# 可以看到 wts 和w_rid是不断在变化的

# 从发起程序这里可以看到，是从这个js文件中加载进来的
# 搜素w_rid可以得到，发现是一个MD5加密
# wts其实就是一个时间戳
import time

now=time.time()
# print(int(now)) 可以得到wts

# 进行断点测试
# 断点以后刷新，发现界面卡住了，然后也没有评论链接加载出来
# 恢复执行以后，发现是由评论的，因此猜测成立

# 往下滑动，就会发现，又卡住了，其实就是在加载下一个评论的链接的时候受到了拦截
# 恢复执行，马上就有链接出来了
"""w_rid:md5(Ut+ct)"""
# 因此需要知道 Ut 和 ct

Ut="""mode=3&oid=366804595&pagination_str=%7B%22offset%22%3A%22%7B%5C%22type%5C%22%3A1%2C%5C%22direction%5C%22%3A1%2C%5C%22session_id%5C%22%3A%5C%221742623236179632%5C%22%2C%5C%22data%5C%22%3A%7B%7D%7D%22%7D&plat=1&type=1&web_location=1315875&wts=1701780625"""
# 其实ct是一个定值，可以一直使用的
ct="ea1db124af3c7062474693fa704f4ff8"
# 为什么pagination_str变成这样 点击查看URL码就发现了
# 因此，pagination_str还要转成URL码的形式，解码以后是一样的

# 可以验证一下是不是
# 现在验证w_rid
# print(Ut+ct)

# 加密后的
# 8CF57E756B3846204744FD39ACE878BA 不能加空格，
# 366174E8897D6905987A72DFCE15ED01
# 这个是对比的
# 366174e8897d6905987a72dfce15ed01
# 然后发现是一样的 因此破解成功
# 366174e8897d6905987a72dfce15ed01
wts=int(time.time())


import urllib
from urllib import parse


pl='%7B%22offset%22%3A%22%7B%5C%22type%5C%22%3A1%2C%5C%22direction%5C%22%3A1%2C%5C%22session_id%5C%22%3A%5C%221742623236179632%5C%22%2C%5C%22data%5C%22%3A%7B%7D%7D%22%7D'


txt=urllib.parse.unquote(pl)
print(txt)
txt2=urllib.parse.quote(txt)
print(txt2)


from hashlib import md5

print(md5((Ut+ct).encode(encoding='utf-8')).hexdigest())





"""
oid: 875789979
type: 1
mode: 3
pagination_str: {"offset":""}
plat: 1
seek_rpid: 
web_location: 1315875
w_rid: c42d9a8812fff06fd4e8be4b7b1d6a37
wts: 1701835305
"""

"""
oid: 875789979
type: 1
mode: 3
pagination_str: {"offset":"{\"type\":1,\"direction\":1,\"session_id\":\"1742679360401344\",\"data\":{}}"}
plat: 1
web_location: 1315875
w_rid: 02f51fffa258c20a2c0d73b6deab29c0
wts: 1701835353
"""


"""
oid: 536379350
type: 1
mode: 3
pagination_str: {"offset":"{\"type\":1,\"direction\":1,\"session_id\":\"1742679455205980\",\"data\":{}}"}
plat: 1
web_location: 1315875
w_rid: e70bf9e15763ba73f3fff02ac89308ba
wts: 1701835413
"""