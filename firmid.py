# -*- coding: utf-8 -*-
import requests
import re
import time
import random
import math
import os
from lxml import etree
import xlrd
from selenium import webdriver
data = xlrd.open_workbook("VC list 2000-2016 .xlsx")
table = data.sheets()[1]  # 0表示excel第一张sheet表
firm_id = table.col_values(0)  # 获取excel第一列中的所有值并保存为列表
firm_name = table.col_values(1)
firm_address = table.col_values(2)

agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
url = 'https://www.qichacha.com/search?key='
url2 = 'https://www.qichacha.com/firm_6a32ccc355c8e66df4f420e09a2bd06b.shtml'
headers = {
        "User-Agent": agent,
        'Cookie':'gr_user_id=1d7b3652-9b7b-48df-8ddc-825fe3ec7ab9; _uab_collina=150002971511674392649455; UM_distinctid=15d40bd03194f-0971ef3e6337bf-8383667-144000-15d40bd031b315; PHPSESSID=4qd728lc2qhcv76pkfei32u280; acw_tc=AQAAAC10pCGt8g4A9xxTctqj9BCaNO7q; _umdata=535523100CBE37C3B7BC22BA12D817113DE1416F13F8AB402AC8B08ACA00A8F9BA3F9AEF20F36874CD43AD3E795C914C5A171D69718737F3DF27DC613986006D; gr_session_id_9c1eb7420511f8b2=cf05394c-a274-49b9-a8ba-9363551391ff; gr_cs1_cf05394c-a274-49b9-a8ba-9363551391ff=user_id%3Adf713ee8d7355737ee182a56bec3ee9f; CNZZDATA1254842228=1956589661-1500024653-%7C1500473133'
            }

def crawl_firm_code(key_1,key_2):
    try:
        result = requests.get(key_1,headers=headers,timeout = 20).text
        time.sleep(30)
        #result = chrome.get(key_1).text
        #print(result)
        if '小查还没找到数据' in result:
            result = requests.get(key_2,headers=headers,timeout = 20).text
            time.sleep(30)
            if '小查还没找到数据' in result:
                firm_code = '无'
            else:
                pattern = r'<a href="/firm_(.*?).shtml'
                firm_code = re.findall(pattern, result, re.S)[0]
            #result = chrome.get(key_2).text
           # print(result)
        else:
            pattern = r'<a href="/firm_(.*?).shtml'
            firm_code = re.findall(pattern, result, re.S)[0]
    except Exception as e:
        print(e)
        firm_code = '出错了'
    return firm_code

#detect_url = 'http://httpbin.org/ip'
#proxies = crawlproxy()
for i in range(6352,len(firm_id)):
    f = open('VC公司详细资料代码.txt', 'a', encoding='utf-8')
    key_1  = url+firm_name[i] +'+'+ firm_address[i]
    key_2 = url + firm_name[i]
    #try:
    firm_key = crawl_firm_code(key_1, key_2)
    # except Exception as e:
    #     firm_code = '无'
    print(firm_name[i]+'---'+firm_key)
    f.write(str(firm_id[i])+']'+firm_name[i]+']'+firm_address[i]+']'+firm_key)
    f.write('\n')
    f.close()


