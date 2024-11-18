# 生成要抓取的八个城市以及对应岗位的链接
import requests
import pandas as pd


target_code = ['530', '538', '763', '531', '854', '613', '653', '551']

df = pd.read_excel(r'target_url.xlsx', index_col=None)

# print(df)
# https://www.zhaopin.com/sou/jl489/kw01800I00A0
all_url = pd.DataFrame()
careers = []
city_codes = []
urls = []
for i in range(len(df.index)):
    career = df.iloc[i, 0]
    base_url = df.iloc[i, 1]
    keyword = base_url.split("/")[-1]
    # print(keyword)
    print(career, base_url)
    for code in target_code:
        url = f'https://www.zhaopin.com/sou/jl{code}/{keyword}'
        careers.append(career)
        city_codes.append(code)
        urls.append(url)

all_url['职业'] = careers
all_url['城市编码'] = city_codes
all_url['url'] = urls

all_url.to_excel("八个城市的二级目标职位链接.xlsx", index=None)


