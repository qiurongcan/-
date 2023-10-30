# 导入模块
import requests
import xlwt
import re
from lxml import etree
from time import sleep

# 需要修改地方
# url的编号
# 保存文件的文件名


# 生成所有页码的url
urls=[]
# for i in range(1,70):
# 先爬取1-15页的数据，可以分页数爬取数据
# 爬取15-30
# 爬取30-45
# 爬取45-60
# 爬取60-70

# 先爬取5页数据测试
# 已完成1-5
# 已完成6-10
# 已完成11-20
# 已完成21-40  但是被覆盖了
# 41-69 账号被封了

for i in range(41,70):
    url=f'http://muchong.com/bbs/search.php?wd=%B7%C7%C9%FD%BC%B4%D7%DF&fid=0&search_type=thread&adfilter=0&page={i}'
    urls.append(url)

# print(urls)

wb=xlwt.Workbook()
sh=wb.add_sheet(r'信息')
sh.write(0,0,'分类')
sh.write(0,1,'标题')
sh.write(0,2,'详细网址')
sh.write(0,3,'作者')
sh.write(0,4,'发布时间')
sh.write(0,5,'详细内容')


# 定义一个请求第二层网页的爬虫
def get_data(url,headers):
    resp=requests.get(url=url,headers=headers)
    # 先爬取1-14页的数据，可以分页数爬取数据
    # print(resp.text)
    # obj=re.compile(r'<div class="t_fsz">(.*?)</div>',re.S)
    # div=obj.findall(resp.text)
    # print(div)
    # 数据这一块可能只能用re才可以全部爬取了
    # 发现问题了，这个破网站有的时候还需要加上防盗链才可以获取数据，有的是加密了获取不了，好吧
    html=etree.HTML(resp.text)
    td_text=html.xpath(r'//*[@id="pid1"]/tr[1]/td[2]//div[@class="t_fsz"]//td[@valign="top"]//text()')
    td_text=''.join(td_text).replace(r'\r\n','')
    # td=div[0].xpath(r'.//*/text()')
    # //*[@id="pid1"]/tr[1]/td[2]/div/div[3]/table/tbody/tr/td/br[2]
    # 需要关闭网页
    resp.close()
    return td_text


# 设置请求头 需要加上cookie和refer
# header={
#     "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.69",

# }
# header 中需要修改cookie，会出现账号被封锁的情况
header={
    # "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.69",
    # "Referer":"http://muchong.com/bbs/qing_search.php?",
    # 使用新的cookie
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.76",
    "Referer":"http://muchong.com/bbs/logging.php?action=login_phone",
    # 可能需要使用一些代理IP进行，爬取，很多内容需要cookie才可以进行访问
    # 明天用自己的台式机试一下
    # "Cookie":"_discuz_in=1; _emuch_index=1; _discuz_uid=34102572; _discuz_pw=a668203d9bd8b50f; discuz_tpl=qing; _last_fid=6; view_tid=15863012; _discuz_cc=67961066146483607; last_ip=39.96.119.215_34102572",
    "Cookie":"_discuz_in=1; _discuz_cc=14961636146002774; last_ip=39.96.119.197_34102572; acw_tc=276077db16943450913851033e5d854a4eb4a1efe1258eab77e7ad93d62915; _emuch_index=1;",
    "Cookie":"_discuz_in=1; _emuch_index=1; discuz_tpl=qing; guest_view_tid=15479060; acw_tc=276077cf16944012493637107edc2e3c6234ae4ca7d032e9f482233fc78e51; _discuz_uid=34120591; _discuz_pw=ce022c6d15e7094c; last_ip=39.96.119.207_34120591; view_tid=15479060; _discuz_cc=46961420444344146",
}

# 用于书写excel的flag
k=1


print("--------开始爬取数据--------")



for url in urls:
    # 请求数据
    try:
        resp=requests.get(url=url,headers=header)
        # 解析数据，使用xpath 解析数据
        html_data=etree.HTML(resp.text)
        table1=html_data.xpath(r'/html/body//table[@border="0"]')
        tbodys=table1[1].xpath(r'./tbody')
        # 测试是否获取数据
        # print(tbodys)
        for tbody in tbodys:
        # 会出现空白行，如果有空白行，则需要跳过
            classify=tbody.xpath(r'./tr/td/a//text()')
            href=tbody.xpath(r'./tr/th//a/@href')
            title=tbody.xpath(r'./tr/th//a//text()')
            author=tbody.xpath(r'tr/td/span/a/text()')
            publishTime=tbody.xpath(r'./tr/td[@width="120"]/nobr/text()')
            
            # 需要关闭网页
            resp.close()
            # 需要跳过空白行
            if len(classify)!=0:
                # 需要将列表转化为文字
                sh.write(k,0,classify[0])
                sh.write(k,1,href[0])
                title=''.join(title)
                sh.write(k,2,title)
                sh.write(k,3,author[0])
                sh.write(k,4,publishTime[0].replace(r"\n\t\t\t\n\n",''))
                text=get_data(url=href[0],headers=header)
                # print(text)
                sh.write(k,5,text)
                print(f'---完成第{k}次数据爬取---')
                k+=1
                # 设置一下延迟，减缓爬取数据的速度
                sleep(3)

    except:
        break

            
    # break
wb.save('小木虫_21-40.xls')
print("--------爬取完成--------")
