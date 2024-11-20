# 获取简要的信息，一页20个数据的情况

import logging
import os
from datetime import datetime
import pandas as pd
from crawl_one_career import get_career_details
from tqdm import tqdm
from time import sleep

# 创建一个文件夹用于保存每页的原始数据
save_origin_floder = r'./jobFileList'
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

def get_all_urls(file_path, headers):
    """
    Args:
        file_path: 存储目标链接的文件路径
    """
    df = pd.read_excel(file_path)

    result_df = pd.DataFrame()

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
            for j in tqdm(range(2), desc="[Job List]", leave=False):
                target_url = url + f"/p{j+1}"
                try:
                    
                    job_dict, origin_data = get_career_details(url=target_url, headers=headers)
                    # print(result)
                    origin_data.to_json(f'{save_origin_floder}/{career}-{cityId}-p{j+1}.json')
                    logger.info(f'page{j+1} is successed!')
                    temp_df = pd.DataFrame(job_dict)
                    result_df = pd.concat([result_df, temp_df], axis=0)
                    sleep(2)
                    break

                except:
                    logger.error(f'page{j+1} can not get')
            
            


            result_df.to_excel(r'两页所有职位链接测试.xlsx', index=None)
            
            phar.update(1)

            sleep(2)
            break
        


if __name__ == "__main__":

    file_path = r'八个城市的二级目标职位链接.xlsx'
    # 放在外面方面更新cookie
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        "cookie": "_uab_collina=173194434492855344221263; __tst_status=1603720322#; x-zp-client-id=43d8cb51-ebe7-4a6c-b22b-3a496e021ce8; FSSBBIl1UgzbN7NS=5E37ctZCQWCaXRaFysG2hdjYZif6Qw4OZ8u1LkqehVXdh0pSYKczobJ9loxCCiWabU0vrBHSH76ngFhrql6XGka; FSSBBIl1UgzbN7NT=5RuzINKQ4U_LqqqDsHddVeG307XAC2yFrJi9CnECzOe51cr5TYZTEgj26XrFDmT3Mz1PpzvkZPrufJMI1KL1YSuAVStqkATw82MUkASS76mGQKKzMJDojzZD8vls18m.Nhs9M1_3zijfbkPymEPEkYYPvNItRvnZfF5lxwp3d4SXToaHj3Dfo90xN.Qrk4JQ7reQJxqzd7oLf5fOf6XxU85Dcp2MjI6QnuXxfSWJViI4seID6z4DwbkRZKrYvtXK4u948XDitLIYrRqofq025fUCrrh.4jGkVtODwfYHJAjqIESwCT6INMb9iqWyOMk_oTatmuLo7iK4Sv_MTazoyAO; LastCity=%E8%A5%BF%E5%AE%89; LastCity%5Fid=854; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221149139192%22%2C%22first_id%22%3A%221933fed6c78cc8-09d27d27d27d28-7e433c49-1296000-1933fed6c791e8a%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fcn.bing.com%2F%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkzM2ZlZDZjNzhjYzgtMDlkMjdkMjdkMjdkMjgtN2U0MzNjNDktMTI5NjAwMC0xOTMzZmVkNmM3OTFlOGEiLCIkaWRlbnRpdHlfbG9naW5faWQiOiIxMTQ5MTM5MTkyIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%221149139192%22%7D%2C%22%24device_id%22%3A%221933fed6c78cc8-09d27d27d27d28-7e433c49-1296000-1933fed6c791e8a%22%7D; sensorsdata2015jssdkchannel=%7B%22prop%22%3A%7B%22_sa_channel_landing_url%22%3A%22%22%7D%7D; _uab_collina=173211628170782734208922; 1420ba6bb40c9512e9642a1f8c243891=ba369792-c421-4f25-98f7-d7b5b03bf720; locationInfo_search={%22code%22:%22857%22%2C%22name%22:%22%E5%92%B8%E9%98%B3%22%2C%22message%22:%22%E5%8C%B9%E9%85%8D%E5%88%B0%E5%B8%82%E7%BA%A7%E7%BC%96%E7%A0%81%22}",
        # "cookie": "__tst_status=2201893872#; _uab_collina=173194434492855344221263; x-zp-client-id=43d8cb51-ebe7-4a6c-b22b-3a496e021ce8; FSSBBIl1UgzbN7NS=5E37ctZCQWCaXRaFysG2hdjYZif6Qw4OZ8u1LkqehVXdh0pSYKczobJ9loxCCiWabU0vrBHSH76ngFhrql6XGka; locationInfo_search={%22code%22:%222373%22%2C%22name%22:%22%E8%A5%BF%E5%AE%89%E5%9B%BD%E5%AE%B6%E6%B0%91%E7%94%A8%E8%88%AA%E5%A4%A9%E4%BA%A7%E4%B8%9A%E5%9F%BA%E5%9C%B0%22%2C%22message%22:%22%E5%8C%B9%E9%85%8D%E5%88%B0%E5%B8%82%E7%BA%A7%E7%BC%96%E7%A0%81%22}; zp_passport_deepknow_sessionId=5252fecfs7eee74870b658ecb50e4e265ead; FSSBBIl1UgzbN7NT=5RuzINKQ4U_LqqqDsHddVeG307XAC2yFrJi9CnECzOe51cr5TYZTEgj26XrFDmT3Mz1PpzvkZPrufJMI1KL1YSuAVStqkATw82MUkASS76mGQKKzMJDojzZD8vls18m.Nhs9M1_3zijfbkPymEPEkYYPvNItRvnZfF5lxwp3d4SXToaHj3Dfo90xN.Qrk4JQ7reQJxqzd7oLf5fOf6XxU85Dcp2MjI6QnuXxfSWJViI4seID6z4DwbkRZKrYvtXK4u948XDitLIYrRqofq025fUCrrh.4jGkVtODwfYHJAjqIESwCT6INMb9iqWyOMk_oTatmuLo7iK4Sv_MTazoyAO; at=bfb028b239ef4dd4aca984eb8f91eb68; rt=53f423dafb554a3abba5afc97ef517f1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221149139192%22%2C%22first_id%22%3A%221933fed6c78cc8-09d27d27d27d28-7e433c49-1296000-1933fed6c791e8a%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkzM2ZlZDZjNzhjYzgtMDlkMjdkMjdkMjdkMjgtN2U0MzNjNDktMTI5NjAwMC0xOTMzZmVkNmM3OTFlOGEiLCIkaWRlbnRpdHlfbG9naW5faWQiOiIxMTQ5MTM5MTkyIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%221149139192%22%7D%2C%22%24device_id%22%3A%221933fed6c78cc8-09d27d27d27d28-7e433c49-1296000-1933fed6c791e8a%22%7D; LastCity=%E8%A5%BF%E5%AE%89; LastCity%5Fid=854; ZL_REPORT_GLOBAL={%22jobs%22:{%22recommandActionidShare%22:%22903c2761-a557-4934-b401-cb6be5339517-job%22}}",
    }

    get_all_urls(file_path=file_path, headers=headers)









