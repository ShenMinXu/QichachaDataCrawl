# -*- coding: utf-8 -*-
import requests
import re
import time
import random
import math
import os
from lxml import etree
import xlrd
def baseinformation(firmname,result_firm_name,selector):
    filename = 'baseinformation.txt'
    base_info = selector.xpath('//html/body/section[starts-with(@class,"panel b-a base_info")]')
    result = base_info[0].xpath('string(.)')
    result = re.sub(r'\n|\s|工商信息|对外投资与任职 >|查看地图|附近公司', '', result)
    result = re.sub(r'统一社会信用代码：', ']统一社会信用代码：', result)
    result = re.sub(r'纳税人识别号：', ']纳税人识别号：', result)
    result = re.sub(r'注册号：', ']注册号：', result)
    result = re.sub(r'组织机构代码：', ']组织机构代码：', result)
    result = re.sub(r'负责人：', ']负责人：', result)
    result = re.sub(r'法定代表人：', ']法定代表人：', result)
    result = re.sub(r'注册资本：', ']注册资本：', result)
    result = re.sub(r'经营状态：', ']经营状态：', result)
    result = re.sub(r'成立日期：', ']成立日期：', result)
    result = re.sub(r'公司类型：', ']公司类型：', result)
    result = re.sub(r'人员规模：', ']人员规模：', result)
    result = re.sub(r'营业期限：', ']营业期限：', result)
    result = re.sub(r'登记机关：', ']登记机关：', result)
    result = re.sub(r'核准日期：', ']核准日期：', result)
    result = re.sub(r'英文名：', ']英文名：', result)
    result = re.sub(r'所属地区', ']所属地区', result)
    result = re.sub(r'所属行业', ']所属行业', result)
    result = re.sub(r'企业地址：', ']企业地址：', result)
    result = re.sub(r'经营范围：', ']经营范围：', result)
    f = open(filename,'a',encoding='utf-8')
    f.write(firmname+']'+result_firm_name+']'+'基本信息'+']'+result)
    f.write('\n')
    f.close()
def Sockinfo(firmname,result_firm_name,selector):
    filename = 'Sockinfo.txt'
    f = open(filename,'a',encoding='utf-8')
    comInfolist = selector.xpath('//*[@id="Sockinfo"]/table/tr')
    for i in range(1,len(comInfolist)):
        result = ''
        all = comInfolist[i].xpath('td')
        for j in range(0,len(all)):
            text = all[j].xpath('string(.)')
            text = re.sub(r'\s|\n|对外投资与任职 >','',text)
            result = result +']'+text
        f.write(firmname+']'+result_firm_name+']'+'股东信息'+']'+result)
        f.write('\n')
    f.close()
def Mainmember(firmname,result_firm_name,selector):
    filename = 'Mainmember.txt'
    f = open(filename,'a',encoding = 'utf-8')
    mainmember = selector.xpath('//*[@id="Mainmember"][1]/table/tr')
    for i in range(1,len(mainmember)):
        result1 = mainmember[i].xpath('td')[0]
        result2 = mainmember[i].xpath('td')[1]
        member = result1.xpath('string(.)')
        member = re.sub(r'\s|\n|对外投资与任职 >','',member)
        job = result2.xpath('string(.)')
        job = re.sub(r'\s|\n','',job)
        f.write(firmname+']'+result_firm_name+']'+'主要成员'+']'+member+']'+job)
        f.write('\n')
def Changelist(firmname,result_firm_name,selector):
    #table_name = 'mistake'
    filename = 'changelist.txt'
    f = open(filename,'a',encoding='utf-8')
    changelist = selector.xpath('//*[@id="Changelist"]/table/tr')
    changelist_type ='变更类型'
    k = 1
    if k > len(changelist):
        print(firmname+'无变更记录')
        #print(content)
    while k < len(changelist):
        html = etree.tostring(changelist[k])
        if 'id="ma_twoword"' in str(html):
            changelist_type  = changelist[k].xpath('string(.)')
            k = k + 2
        else:
            all_result = changelist[k].xpath('td')
            result = ''
            for each in all_result:
                result0 = each.xpath('string(.)')
                result0 =re.sub(r'\s|\n|对外投资与任职>','',result0)
                result = result +']'+result0
            #print(result)
            f.write(firmname+']'+result_firm_name+']'+'变更记录'+']'+changelist_type+']'+result)
            f.write('\n')
            k = k+1
    f.close()
def Comintroduce(firmname,result_firm_name,selector):
    filename = 'Comintroduce.txt'
    f = open(filename, 'a', encoding='utf-8')
    comintroduce = selector.xpath('//*[@id="Comintroduce"]/div[2]')[0]
    result = comintroduce.xpath('string(.)')
    result = re.sub(r'\n|\s', '', result)
    #print(result)
    f.write(firmname + ']'+result_firm_name+']'+'简介'+']' + result)
    f.write('\n')
    f.close()
def Subcom(firmname,result_firm_name,selector):
    filename = 'Subcom.txt'
    f = open(filename, 'a', encoding='utf-8')
    subcom = selector.xpath('//*[@id="Subcom"]/div[2]/ul/li')
    for i in range(0, len(subcom)):
        result = subcom[i].xpath('string(.)')
        result = re.sub(r'\s|\n', ']', result)
        #print(result)
        f.write(firmname + ']'+result_firm_name+']'+'分支机构'+']' + result)
        f.write('\n')
    f.close()

# f = open('2333.txt',encoding= 'utf-8')
# content = f.read()
# #print(content)
# selector = etree.HTML(content)
# pattern = r'onclick="findRelation\(\'(.*?)\','
# result_firm_name = re.findall(pattern, content, re.S)[0]
# firm_name = 'a'
# Changelist('aa','22',selector)




data = xlrd.open_workbook("VC公司详细资料代码.xlsx")
table = data.sheets()[1]  # 0表示excel第一张sheet表
firm_name = table.col_values(1)  # 获取excel第一列中的所有值并保存为列表
firm_code = table.col_values(3)
new_firm_name =table.col_values(4)
agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
headers = {
        "User-Agent": agent,
        'Cookie':'gr_user_id=1d7b3652-9b7b-48df-8ddc-825fe3ec7ab9; _uab_collina=150002971511674392649455; UM_distinctid=15d40bd03194f-0971ef3e6337bf-8383667-144000-15d40bd031b315; acw_tc=AQAAAHGn4Ek2sAsA9xxTci7Z+rG48znx; PHPSESSID=vvth2jhg18r9uvdck0fak2fqi0; _umdata=535523100CBE37C3B7BC22BA12D817113DE1416F13F8AB402AC8B08ACA00A8F9BA3F9AEF20F36874CD43AD3E795C914C4941177A9F6206B5E1D1B55C91B532EB; gr_session_id_9c1eb7420511f8b2=21d03f3f-ba26-41f9-974a-95d02bfa35fe; gr_cs1_21d03f3f-ba26-41f9-974a-95d02bfa35fe=user_id%3Adf713ee8d7355737ee182a56bec3ee9f; CNZZDATA1254842228=1956589661-1500024653-%7C1501069909'
}
for i in range(5593,5594):
    url = 'https://www.qichacha.com/company_getinfos?unique='+firm_code[i]+'&companyname='+firm_name[i]+'&tab=base'
    urltest = 'https://www.qichacha.com/firm_'+firm_code[i]+'.shtml'
    try:
        test = requests.get(urltest,headers=headers,timeout=60).text
        time.sleep(1)
        content = requests.get(url,headers=headers,timeout = 20).text
        selector = etree.HTML(content)
        pattern = r'onclick="findRelation\(\'(.*?)\','
        pattern2 = r'<meta name="author" content="leslie"> <title>(.*?)工商信息'
        result_firm_name = re.findall(pattern2, test, re.S)[0]
        #result_firm_name = new_firm_name[i]
        # if new_firm_name[i] in test:
        #     aaaa=2
        # else:
        #     print(ddd[9])
        #result_firm_name = ''
    except Exception as e:
        print(e)
        print(firm_name[i]+'出错----------------------------------')
        f= open('访问出错公司.txt','a',encoding='utf-8')
        f.write(firm_name[i]+' '+firm_code[i])
        f.write('\n')
        f.close()
        time.sleep(30)
        continue

    # try:
    #     baseinformation(firm_name[i],result_firm_name,selector)
    # except Exception as e:
    #     print(firm_name[i]+'无基本信息')
    # try:
    #     Sockinfo(firm_name[i], result_firm_name, selector)
    # except Exception as e:
    #     print(firm_name[i] + '无股东信息')
    # try:
    #     Mainmember(firm_name[i], result_firm_name, selector)
    # except Exception as e:
    #     print(firm_name[i] + '无主要成员信息')
    try:
        Changelist(firm_name[i], result_firm_name, selector)
    except Exception as e:
        print(firm_name[i] + '无变更记录')
    try:
        Subcom(firm_name[i], result_firm_name, selector)
    except Exception as e:
        print(firm_name[i] + '无分支机构')
    try:
        Comintroduce(firm_name[i], result_firm_name, selector)
    except Exception as e:
        print(firm_name[i] + '无公司简介')
    #print(firm_name[i] + '爬取成功')
    time.sleep(30)







