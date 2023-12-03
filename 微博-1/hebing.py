# 合并 完整版本 文件夹下的所有excel表格

import os
import pandas as pd

# 指定包含Excel文件的文件夹路径
folder_path = '完整版本'

# 获取文件夹中所有的Excel文件
excel_files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx') or f.endswith('.xls')]

# 创建一个空的DataFrame用于存储合并后的数据
merged_df = pd.DataFrame()

# 遍历每个Excel文件并将其合并到一个DataFrame中
for file in excel_files:
    file_path = os.path.join(folder_path, file)
    df = pd.read_excel(file_path)
    merged_df = merged_df._append(df, ignore_index=True)

# 可选：保存合并后的DataFrame为一个新的Excel文件
merged_df.to_excel('热搜数据集.xlsx', index=False)
