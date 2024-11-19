# 抓取一个详细页面
import requests
import re
import pandas as pd
from box import Box
import json
from pprint import pprint



def get_detail_msg(url, headers):

    result_dict = {}

    obj = re.compile(r'INITIAL_STATE__=(.*?)</script', re.S)

    resp = requests.get(url=url, headers=headers)
    # print(resp.text)
    result = obj.findall(resp.text)[0]
    # print(result)
    job = Box(json.loads(result))
    # 获取职业号码
    jobNumber = job.jobNumber
    result_dict['jobNumber'] = jobNumber
    # 职位的详细信息
    jobDetail = job.jobInfo.jobDetail

    # ---------------公司的详细信息--------------------
    companyName = jobDetail.detailedCompany.companyName
    result_dict['companyName'] = companyName
    companyNumber = jobDetail.detailedCompany.companyNumber
    result_dict['companyNumber'] = companyNumber
    financingStageName = jobDetail.detailedCompany.financingStageName
    result_dict['financingStageName'] = financingStageName
    industryNameLevel = jobDetail.detailedCompany.industryNameLevel
    result_dict['industryNameLevel'] = industryNameLevel
    companySize = jobDetail.detailedCompany.companySize
    result_dict['companySize'] = companySize
    companyDescription = jobDetail.detailedCompany.companyDescription
    result_dict['companyDescription'] = companyDescription
    industryLevel = jobDetail.detailedCompany.industryLevel
    result_dict['industryLevel'] = industryLevel
    company_url = jobDetail.detailedCompany.url # 公司网址
    result_dict['company_url'] = company_url

    # ---------------职业的详细信息---------------------
    positionName = jobDetail.detailedPosition.positionName # 职位名称
    result_dict['positionName'] = positionName
    welfareLabel = jobDetail.detailedPosition.welfareLabel
    if len(welfareLabel) != 0:
        result_dict['welfareLabel'] = welfareLabel
    else:
        result_dict['welfareLabel'] = None
    workType = jobDetail.detailedPosition.workType
    result_dict['workType'] = workType
    skillLabel = jobDetail.detailedPosition.skillLabel # TODO 字典数据，还需要后续处理
    result_dict['skillLabel'] = skillLabel
    jobDesc = jobDetail.detailedPosition.jobDesc # TODO 包含一些div之类的标签，需要处理
    result_dict['jobDesc'] = jobDesc
    workAddress = jobDetail.detailedPosition.workAddress
    result_dict['workAddress'] = workAddress
    latitude = jobDetail.detailedPosition.latitude
    result_dict['latitude'] = latitude
    longitude = jobDetail.detailedPosition.longitude
    result_dict['longitude'] = longitude
    positionPublishTime = jobDetail.detailedPosition.positionPublishTime
    result_dict['positionPublishTime'] = positionPublishTime
    education = jobDetail.detailedPosition.education
    result_dict['education'] = education
    positionUrl = jobDetail.detailedPosition.positionUrl
    result_dict['positionUrl'] = positionUrl
    salary60 = jobDetail.detailedPosition.salary60
    result_dict['salary60'] = salary60
    positionWorkingExp = jobDetail.detailedPosition.positionWorkingExp
    result_dict['positionWorkingExp'] = positionWorkingExp
    positionWorkCity = jobDetail.detailedPosition.positionWorkCity
    result_dict['positionWorkCity'] = positionWorkCity
    jobTypeLevelName = jobDetail.detailedPosition.jobTypeLevelName
    result_dict['jobTypeLevelName'] = jobTypeLevelName
    subJobTypeLevel = jobDetail.detailedPosition.subJobTypeLevel
    result_dict['subJobTypeLevel'] = subJobTypeLevel
    salaryReal = jobDetail.detailedPosition.salaryReal
    result_dict['salaryReal'] = salaryReal

    return result_dict




if __name__ == "__main__":

    

    # 详细页面的网址
    url = r'http://www.zhaopin.com/jobdetail/CC640181680J40693065605.htm'

    # 还是需要添加cookie, cookie是需要登录以后的cookie
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        # "host": "www.zhaopin.com",
        # "referer": "http://www.zhaopin.com/jobdetail/CC649781480J40460244505.htm",
        "cookie": "__tst_status=1262935945#; x-zp-client-id=7307ef44-cb5a-49fb-91f2-9bfab134589a; _uab_collina=169933426445595596639509; sensorsdata2015jssdkchannel=%7B%22prop%22%3A%7B%22_sa_channel_landing_url%22%3A%22%22%7D%7D; LastCity=%E8%A5%BF%E5%AE%89; LastCity%5Fid=854; locationInfo_search={%22code%22:%222373%22%2C%22name%22:%22%E8%A5%BF%E5%AE%89%E5%9B%BD%E5%AE%B6%E6%B0%91%E7%94%A8%E8%88%AA%E5%A4%A9%E4%BA%A7%E4%B8%9A%E5%9F%BA%E5%9C%B0%22%2C%22message%22:%22%E5%8C%B9%E9%85%8D%E5%88%B0%E5%B8%82%E7%BA%A7%E7%BC%96%E7%A0%81%22}; selectCity_search=530; FSSBBIl1UgzbN7NT=5Ru7_gCQ4iXGqqqDsH4DCya4CxMAA2fnmAeU95C3tibjty3wzwCgaIkEgz3KULywKshx84pQUxb9LqdS9JXmQ4s0xh0OhXvHpBjyuJx2nyUpXq2HVT2r.R_XUyHtT8BtWI20FU67J46MI8mnrR9Vf.MMEvQ0FDNvmWZg1aIonl_3WHOyXQGNIeoOhkDybLw71NrtvBzyIu5O6HGy4rD3wfqxeJPD4uMSAQ0p9Wh5kGgPo0Xa6IG2L3hMR39r2qw2oAC_vJyCiCrz5Owy0Vl1KG_yPXKWDMcfhrOqToq87TSCzgWzRu70Xl_1N6XevyPaUX_aGfWS6_DlshIP62J_Ayz; 1420ba6bb40c9512e9642a1f8c243891=76f2d867-567c-4978-8506-81426ded86f9; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221149139192%22%2C%22first_id%22%3A%2218ba83716c61bbc-07dfe747256f2dc-4c657b58-2073600-18ba83716c7ad9%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMThiYTgzNzE2YzYxYmJjLTA3ZGZlNzQ3MjU2ZjJkYy00YzY1N2I1OC0yMDczNjAwLTE4YmE4MzcxNmM3YWQ5IiwiJGlkZW50aXR5X2xvZ2luX2lkIjoiMTE0OTEzOTE5MiJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%221149139192%22%7D%2C%22%24device_id%22%3A%2218ba83716c61bbc-07dfe747256f2dc-4c657b58-2073600-18ba83716c7ad9%22%7D; zp_passport_deepknow_sessionId=19c9d5f9s0eeee411b8ea8b21ff3869cd479; at=0d0a39cff54941b6a06bf5bbba305174; rt=34fce8040351456e849ce8d6111e3942; ZL_REPORT_GLOBAL={%22jobs%22:{%22recommandActionidShare%22:%228a84bf86-5375-4197-88e8-5a3c86d785f9-job%22}}",
    }

    result = get_detail_msg(url=url, headers=headers)
    pprint(result)
    df = pd.DataFrame(result)
    # TODO 不清楚这里为什么会出现相同的行
    df = df.drop_duplicates(subset=['jobNumber'])
    df.to_excel(r"抓取一个职位的详细信息.xlsx", index=None)
    # print(result)
    

