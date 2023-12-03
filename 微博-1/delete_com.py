# 剔除重复的热搜
import pandas as pd

df=pd.read_excel(r'data2.xlsx')
print(len(df.index))

df=df.drop_duplicates(subset=['热搜主题'])
print(len(df.index))

df.to_excel('non_data2.xlsx',index=None)
