import requests
import re
from pprint import pprint
import json
from box import Box
import pandas as pd
from collections import defaultdict

def get_career_details(url, headers):

    job_dict = defaultdict(list)
    
    obj = re.compile(r'INITIAL_STATE__=(.*?)</script', re.S)

    resp = requests.get(url=url, headers=headers)
    # print(resp.text)
    result = obj.findall(resp.text)[0]
    json_data = Box(json.loads(result))
    job_lists = json_data.positionList
    # print(job_lists)
    # 一共二十个职位，并获取每个职位的具体链接
    for job in job_lists:
        # 1.名片中常见的简要标签
        cardCustomJson = job.cardCustomJson
        job_dict['cardCustomJson'].append(cardCustomJson)
        # 2.
        cityDistrict = job.cityDistrict
        job_dict['cityDistrict'].append(cityDistrict)
        companyName = job.companyName
        job_dict['companyName'].append(companyName)
        companyNumber = job.companyNumber
        job_dict['companyNumber'].append(companyNumber)
        companySize = job.companySize
        education = job.education
        job_dict['companySize'].append(companySize)
        # 上市阶段情况，code并不一定有
        # financingStage_code = job.financingStage.code
        # financingStage_name = job.financingStage.name
        firstPublishTime = job.firstPublishTime
        job_dict['firstPublishTime'].append(firstPublishTime)
        industryName = job.industryName
        job_dict['industryName'].append(industryName)
        jobId = job.jobId
        job_dict['jobId'].append(jobId)
        jobKnowledgeWelfareFeatures = job.jobKnowledgeWelfareFeatures
        job_dict['jobKnowledgeWelfareFeatures'].append(jobKnowledgeWelfareFeatures)
        # print(jobKnowledgeWelfareFeatures)
        
        jobSkillTags = job.jobSkillTags # 
        job_dict['jobSkillTags'].append(jobSkillTags)
        jobSummary = job.jobSummary
        job_dict['jobSummary'].append(jobSummary)
        job_name = job.name
        job_dict['job_name'].append(job_name)
        job_number = job.number
        job_dict['job_number'].append(job_number)
        positionURL = job.positionURL
        job_dict['positionURL'].append(positionURL)
        property = job.property
        job_dict['property'].append(property)
        salary60 = job.salary60
        job_dict['salary60'].append(salary60)
        salaryReal = job.salaryReal
        job_dict['salaryReal'].append(salaryReal)
        workCity = job.workCity
        job_dict['workCity'].append(workCity)
        # print(workCity)
        workType = job.workType
        job_dict['workType'].append(workType)
        workingExp = job.workingExp
        job_dict['workingExp'].append(workingExp)



    # pprint(json_data)
    return job_dict



if __name__ == "__main__":
    # 一页是20个职位
    url = r'https://www.zhaopin.com/sou/jl531/kw01500O80EO062NO0AF8G'
    # 需要使用cookies
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        # "cookie": "__tst_status=2201893872#; _uab_collina=173194434492855344221263; x-zp-client-id=43d8cb51-ebe7-4a6c-b22b-3a496e021ce8; FSSBBIl1UgzbN7NS=5E37ctZCQWCaXRaFysG2hdjYZif6Qw4OZ8u1LkqehVXdh0pSYKczobJ9loxCCiWabU0vrBHSH76ngFhrql6XGka; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221933fed6c78cc8-09d27d27d27d28-7e433c49-1296000-1933fed6c791e8a%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkzM2ZlZDZjNzhjYzgtMDlkMjdkMjdkMjdkMjgtN2U0MzNjNDktMTI5NjAwMC0xOTMzZmVkNmM3OTFlOGEifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%221933fed6c78cc8-09d27d27d27d28-7e433c49-1296000-1933fed6c791e8a%22%7D; sajssdk_2015_cross_new_user=1; locationInfo_search={%22code%22:%222373%22%2C%22name%22:%22%E8%A5%BF%E5%AE%89%E5%9B%BD%E5%AE%B6%E6%B0%91%E7%94%A8%E8%88%AA%E5%A4%A9%E4%BA%A7%E4%B8%9A%E5%9F%BA%E5%9C%B0%22%2C%22message%22:%22%E5%8C%B9%E9%85%8D%E5%88%B0%E5%B8%82%E7%BA%A7%E7%BC%96%E7%A0%81%22}; 1420ba6bb40c9512e9642a1f8c243891=168b2d91-55d6-401b-a97d-2dc2ab479ea3",
        "cookie": "__tst_status=2201893872#; _uab_collina=173194434492855344221263; x-zp-client-id=43d8cb51-ebe7-4a6c-b22b-3a496e021ce8; FSSBBIl1UgzbN7NS=5E37ctZCQWCaXRaFysG2hdjYZif6Qw4OZ8u1LkqehVXdh0pSYKczobJ9loxCCiWabU0vrBHSH76ngFhrql6XGka; locationInfo_search={%22code%22:%222373%22%2C%22name%22:%22%E8%A5%BF%E5%AE%89%E5%9B%BD%E5%AE%B6%E6%B0%91%E7%94%A8%E8%88%AA%E5%A4%A9%E4%BA%A7%E4%B8%9A%E5%9F%BA%E5%9C%B0%22%2C%22message%22:%22%E5%8C%B9%E9%85%8D%E5%88%B0%E5%B8%82%E7%BA%A7%E7%BC%96%E7%A0%81%22}; zp_passport_deepknow_sessionId=5252fecfs7eee74870b658ecb50e4e265ead; FSSBBIl1UgzbN7NT=5RuzINKQ4U_LqqqDsHddVeG307XAC2yFrJi9CnECzOe51cr5TYZTEgj26XrFDmT3Mz1PpzvkZPrufJMI1KL1YSuAVStqkATw82MUkASS76mGQKKzMJDojzZD8vls18m.Nhs9M1_3zijfbkPymEPEkYYPvNItRvnZfF5lxwp3d4SXToaHj3Dfo90xN.Qrk4JQ7reQJxqzd7oLf5fOf6XxU85Dcp2MjI6QnuXxfSWJViI4seID6z4DwbkRZKrYvtXK4u948XDitLIYrRqofq025fUCrrh.4jGkVtODwfYHJAjqIESwCT6INMb9iqWyOMk_oTatmuLo7iK4Sv_MTazoyAO; at=bfb028b239ef4dd4aca984eb8f91eb68; rt=53f423dafb554a3abba5afc97ef517f1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221149139192%22%2C%22first_id%22%3A%221933fed6c78cc8-09d27d27d27d28-7e433c49-1296000-1933fed6c791e8a%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkzM2ZlZDZjNzhjYzgtMDlkMjdkMjdkMjdkMjgtN2U0MzNjNDktMTI5NjAwMC0xOTMzZmVkNmM3OTFlOGEiLCIkaWRlbnRpdHlfbG9naW5faWQiOiIxMTQ5MTM5MTkyIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%221149139192%22%7D%2C%22%24device_id%22%3A%221933fed6c78cc8-09d27d27d27d28-7e433c49-1296000-1933fed6c791e8a%22%7D; LastCity=%E8%A5%BF%E5%AE%89; LastCity%5Fid=854; ZL_REPORT_GLOBAL={%22jobs%22:{%22recommandActionidShare%22:%22903c2761-a557-4934-b401-cb6be5339517-job%22}}",
    }

    # 不登陆只有5页，登陆了可以看到全部的
    job_dict = get_career_details(url=url, headers=headers)

    df = pd.DataFrame(job_dict)

    df.to_excel("20个职位抓取测试.xlsx", index=None)



