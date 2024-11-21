# 获取每一页的详细信息

import os
import pandas as pd
from crawl_detail_url import get_detail_msg
import json
from tqdm import tqdm
import logging
from datetime import datetime
from time import sleep


# 创建一个文件夹用于保存每页的原始数据
save_origin_floder = r'./jobDetails'
os.makedirs(save_origin_floder, exist_ok=True)

# 创建日志文件夹
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

def get_all(path, headers):
    """
    Args:
        path: 链接路径
    """
    df = pd.read_excel(path)

    logger.info("====================获取详细信息======================")

    df_result = pd.DataFrame()
    with tqdm(total=len(df.index), desc="Crawl Process") as phar:
        for i in range(len(df.index)):
            
            
            url = df['positionURL'].iloc[i]
            jobId = df['jobId'].iloc[i]
            job_number = df['job_number'].iloc[i]

            

            phar.set_postfix({
                "job_number": job_number,
            })  
            if i <= 1813:
                continue
            phar.update(1)  

            result = get_detail_msg(url=url, headers=headers)
            
            temp_df = pd.DataFrame(result)
            # 处理重复数据
            temp_df = temp_df.drop_duplicates(subset=['jobNumber'])
            df_result = pd.concat([df_result, temp_df], axis=0)

            logger.info(f'[{i}] {jobId}: {url} is Finished！！！')
            

            # result_df.to_excel(r'所有职位链接测试3.xlsx', index=None)
            
            
            df_result.to_excel(r"最终的详细信息3（全职）.xlsx", index=None)

            # break
            sleep(0.01)



if __name__ == "__main__":

    file_path = r'预投递测试数据（全职）.xlsx'

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        # "host": "www.zhaopin.com",
        # "referer": "http://www.zhaopin.com/jobdetail/CC649781480J40460244505.htm",
        "cookie": "__tst_status=1262935945#; x-zp-client-id=7307ef44-cb5a-49fb-91f2-9bfab134589a; _uab_collina=169933426445595596639509; sensorsdata2015jssdkchannel=%7B%22prop%22%3A%7B%22_sa_channel_landing_url%22%3A%22%22%7D%7D; LastCity=%E8%A5%BF%E5%AE%89; LastCity%5Fid=854; locationInfo_search={%22code%22:%222373%22%2C%22name%22:%22%E8%A5%BF%E5%AE%89%E5%9B%BD%E5%AE%B6%E6%B0%91%E7%94%A8%E8%88%AA%E5%A4%A9%E4%BA%A7%E4%B8%9A%E5%9F%BA%E5%9C%B0%22%2C%22message%22:%22%E5%8C%B9%E9%85%8D%E5%88%B0%E5%B8%82%E7%BA%A7%E7%BC%96%E7%A0%81%22}; selectCity_search=530; FSSBBIl1UgzbN7NT=5Ru7_gCQ4iXGqqqDsH4DCya4CxMAA2fnmAeU95C3tibjty3wzwCgaIkEgz3KULywKshx84pQUxb9LqdS9JXmQ4s0xh0OhXvHpBjyuJx2nyUpXq2HVT2r.R_XUyHtT8BtWI20FU67J46MI8mnrR9Vf.MMEvQ0FDNvmWZg1aIonl_3WHOyXQGNIeoOhkDybLw71NrtvBzyIu5O6HGy4rD3wfqxeJPD4uMSAQ0p9Wh5kGgPo0Xa6IG2L3hMR39r2qw2oAC_vJyCiCrz5Owy0Vl1KG_yPXKWDMcfhrOqToq87TSCzgWzRu70Xl_1N6XevyPaUX_aGfWS6_DlshIP62J_Ayz; 1420ba6bb40c9512e9642a1f8c243891=76f2d867-567c-4978-8506-81426ded86f9; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221149139192%22%2C%22first_id%22%3A%2218ba83716c61bbc-07dfe747256f2dc-4c657b58-2073600-18ba83716c7ad9%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMThiYTgzNzE2YzYxYmJjLTA3ZGZlNzQ3MjU2ZjJkYy00YzY1N2I1OC0yMDczNjAwLTE4YmE4MzcxNmM3YWQ5IiwiJGlkZW50aXR5X2xvZ2luX2lkIjoiMTE0OTEzOTE5MiJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%221149139192%22%7D%2C%22%24device_id%22%3A%2218ba83716c61bbc-07dfe747256f2dc-4c657b58-2073600-18ba83716c7ad9%22%7D; zp_passport_deepknow_sessionId=19c9d5f9s0eeee411b8ea8b21ff3869cd479; at=0d0a39cff54941b6a06bf5bbba305174; rt=34fce8040351456e849ce8d6111e3942; ZL_REPORT_GLOBAL={%22jobs%22:{%22recommandActionidShare%22:%228a84bf86-5375-4197-88e8-5a3c86d785f9-job%22}}",
    }

    get_all(path=file_path, headers=headers)


