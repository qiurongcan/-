# 智联招聘爬取
## 1 爬取主页面的信息

### 1.1 获取每个城市的编码
求职的热门城市配置文件如下：
```python
hotcity.json
```
部分信息格式如下，获取一级城市，暂时省略其他信息
```json
{
    "en_name": "BEIJING",
    "code": "530",
    "name": "北京",
    "type": "MUNICIPALITY",
    "delete": false,
    "sublist": ""
}
```
只需要获取其中的code即可
### 1.2获取二级目标职位的编码信息
如代码`crawl_first.py`文件所示, 该文件抓取了职业编码，例如  
```python
java开发 -> https://www.zhaopin.com/sou/jl489/kw01500O80EO062NO0AF8G
深度学习 -> https://www.zhaopin.com/sou/jl489/kwDNOLT9IRCP760
...
```
其中最后的字符串即职位编码  
因此,可以获取全部二级职位的编码  
最后结果存储在`智联八个类别专业分类以及每个类别职业信息.xlsx`中



### 1.3通过城市编码和职位编码组合目标链接
组合目标链接的代码如`gen_second_url.py`所示
首先明确目标链接的样式, 如下
```python
"""
Args:
    code: 城市编码, For example, 北京 -> 530, 上海 -> 538
    keyword: 在1.2提到的职位编码
"""
url = f'https://www.zhaopin.com/sou/jl{code}/{keyword}'
```
对应组合填充即可, 最后的生成文件如`八个城市的二级目标职位链接.xlsx`所示

## 2 爬取一个职业的一页Job_list(20个职位)
备注: 
1. 没有登录智联的话, 只能获取5页信息
2. 设置headers时,需要定期更换cookie,防止cookie过期

爬取的代码如`crawl_one_career.py`所示,一页可以获取20个职位,但是这个职位在**职位详细描述中不够全面,只有部分信息**
如果需要获取详细信息,需要专门对每个职位进行抓取

抓取的结果如`20个职位抓取测试.xlsx`所示


## 3 对一个求职链接进行详细的抓取
备注:
1. 所有信息存储在页面的源代码中
2. 设置headers时,需要使用cookie,而且是登录以后的cookie,否则会什么都获取不到

在解析页面时,所有信息都以json的格式存储, 存储结构如`job_details.json`所示.  
按照这个json格式解析即可

抓取的代码如`crawl_detail_url.py`所示,最后的结果存储在`抓取一个职位的详细信息.xlsx`中




