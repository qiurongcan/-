# 爬取豆瓣电影Top250
# 需要爬取的信息有：
# -电影名称
# -电影评分
# -评价人数
# -电影简介
# 需要导入的模块 requsets、xml
# 安装方法
# pip3 install requests pandas -i https://pypi.tuna.tsinghua.edu.cn/simple
# 打开终端安装，
import requests
import pandas as pd  #用于保存数据用的
from lxml import etree

# 创建存储的表格
df=pd.read_excel(r'表格.xlsx')

# 找目标网站
# 这个25是关键，一共有250条数据，就一共是10页，一耶是25条，第一耶开头为0，第二耶为25，
# 以此类推，最后一页就是225，那个filter可以不用管，点进去可以的
url=r'https://movie.douban.com/top250?start='
# 存储所有要爬取的url
urls=[]
# 组合url
for i in range(0,250,25):
    urls.append(f'https://movie.douban.com/top250?start={i}')

# print(urls)
# ok
# 1-开始获取数据
# 这里需要设置请求头,点击F12进入,复制user-agent就可以啦
header={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.69"
}
# 创建一个列表来存储所有名字
names=[]
peoples=[]
values=[]
directors=[]
for url in urls:
    resp=requests.get(url=url,headers=header)
    # print(resp.text)
    # 可以发现获取数据成功，现在就是解析数据
    html_data=etree.HTML(resp.text)
    # 使用xpath方法进行提取数据,如何获取xpath路径
    # 用这个li的来比较，然后删除后面的标号
    # /html/body/div[3]/div[1]/div/div[1]/ol/li[1]
    name=html_data.xpath(r'/html/body/div[3]/div[1]/div/div[1]/ol/li/div/div[2]/div[1]/a/span[1]/text()')
    # 发现名字存储再一个列表中了
    # print(name)
    # 成功了，如何获取一页的数据呢
    people=html_data.xpath(r'/html/body/div[3]/div[1]/div/div[1]/ol/li/div/div[2]/div[2]/div/span[4]/text()')
    value=html_data.xpath(r'/html/body/div[3]/div[1]/div/div[1]/ol/li/div/div[2]/div[2]/div/span[2]/text()')
    director=html_data.xpath(r'//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[2]/p[1]/text()')
    # 这里将apped修改为extend即可，导演有点问题，注销了即可
    names.extend(name)
    peoples.extend(people)
    values.extend(value)
    # directors.extend(director)

df['名字']=names
df['评价人数']=peoples
df['评分']=values
# df['导演']=directors

# 保存到豆瓣1中
df.to_excel(r'豆瓣1.xlsx',index=None)
print('爬取完成~~~')
# 这里需要创建一个表格

# okok爬取完成