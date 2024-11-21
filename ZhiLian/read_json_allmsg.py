import os 
from box import Box
import pandas as pd


base_path = r'AllDetailMsg'
json_files = os.listdir(base_path)


result_df = pd.DataFrame()
for p in json_files:
    result_dict = {}
    path = os.path.join(base_path, p)

    job = Box.from_json(filename=path)

    jobNumber = job.jobNumber
    result_dict['jobNumber'] = jobNumber

    # 使用工作ID命名，因为是唯一的
    # job.to_json(f'{default_save_folder}/{jobNumber}.json')

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
    # 雇佣类型
    result_dict['bestEmployerType'] = jobDetail.detailedCompany.bestEmployerType


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
    # 工作地点
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
    # 工作地点Id
    positionCityId = jobDetail.detailedPosition.positionCityId
    result_dict['positionCityId'] = positionCityId

    positionWorkCity = jobDetail.detailedPosition.positionWorkCity
    result_dict['positionWorkCity'] = positionWorkCity

    jobTypeLevelName = jobDetail.detailedPosition.jobTypeLevelName
    result_dict['jobTypeLevelName'] = jobTypeLevelName
    subJobTypeLevel = jobDetail.detailedPosition.subJobTypeLevel
    result_dict['subJobTypeLevel'] = subJobTypeLevel
    salaryReal = jobDetail.detailedPosition.salaryReal
    result_dict['salaryReal'] = salaryReal

    subJobType = jobDetail.detailedPosition.subJobType
    result_dict['subJobType'] = subJobType
    positionStatus = jobDetail.detailedPosition.positionStatus
    result_dict['positionStatus'] = positionStatus
    positionNumber = jobDetail.detailedPosition.positionNumber
    result_dict['positionNumber'] = positionNumber
    positionCityDistrict = jobDetail.detailedPosition.positionCityDistrict
    result_dict['positionCityDistrict'] = positionCityDistrict

    # 需要招聘的人数
    recruitNumber = jobDetail.detailedPosition.recruitNumber
    result_dict['recruitNumber'] = recruitNumber
    temp_df = pd.DataFrame(result_dict)
    temp_df = temp_df.drop_duplicates(subset=['jobNumber'])
    result_df = pd.concat([result_df, temp_df], axis=0)

result_df.to_excel("最终的详细信息6（全职）.xlsx")
