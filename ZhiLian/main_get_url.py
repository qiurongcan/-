# 获取简要的信息，一页20个数据的情况

import logging
import os
from datetime import datetime
import pandas as pd
from crawl_one_career import get_career_details
from tqdm import tqdm
from time import sleep

log_dir = './logs'
os.makedirs(log_dir, exist_ok=True)

# 获取当前日期作为日志文件名
current_date = datetime.now().strftime('%Y-%m-%d')
log_file = os.path.join(log_dir, f'{current_date}.log')
logger = logging.getLogger("crawl_logger")
logger.setLevel(logging.INFO) # 设置日志级别

# 设置文件处理器
file_handler = logging.FileHandler(log_file, encoding='utf-8')
file_handler.setLevel(logging.INFO)

# 创建格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def get_all_urls(file_path, headers):
    """
    Args:
        file_path: 存储目标链接的文件路径
    """
    df = pd.read_excel(file_path)
    with tqdm(total=len(df.index), desc="Crawl Process") as phar:
        for i in range(len(df.index)):
            
            career = df.iloc[i, 0]
            cityId = df.iloc[i, 1]
            url = df.iloc[i,2]

            phar.set_postfix({
                "Career": career,
                "cityId": cityId
            })

            logger.info("----------------------一个类别爬取的分割线------------------------")
            logger.info(f'Career: {career}, cityId: {cityId}, url: {url}')

            # 现在需要组合成不同的页数
            for j in tqdm(range(50), desc="[Job List]", leave=False):
                target_url = url + f"/p{j+1}"
                try:
                    
                    result = get_career_details(url=target_url, headers=headers)
                    # print(result)
                    logger.info(f'page{j+1} is successed!')

                except:
                    logger.error(f'page{j+1} can not get')


            
            phar.update(1)

            sleep(1)
        


if __name__ == "__main__":

    file_path = r'八个城市的二级目标职位链接.xlsx'
    # 放在外面方面更新cookie
    headers = {}

    get_all_urls(file_path=file_path, headers=headers)







