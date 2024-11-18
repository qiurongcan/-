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

