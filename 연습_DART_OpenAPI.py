# pip install OpenDartReader
# pip install pykrx
# pip install Financial # 야후 것 지금은 좀 오바라 생략

# ref: https://opendart.fss.or.kr/
# ref: https://github.com/FinanceData/OpenDartReader
# ref: https://nbviewer.org/github/FinanceData/OpenDartReader/blob/master/docs/OpenDartReader_reference_manual.ipynb # 속성 안내
# ref: https://github.com/sharebook-kr/pykrx
                                                            # (상장기업정보)
# ref: http://comp.fnguide.com/SVO2/ASP/SVD_Finance.asp?gicode=A035420&NewMenuID=103 # pykrx에서 상장된 정보 볼 수 있음

# 오늘 할 것
# 1) 네이버 재무제표 : 상장된 것만 보임(주소에 상장 코드 들어감)
# 2) 다트 재무제표 : API 쓰는 형태

import numpy as np
import pandas as pd
import requests
import OpenDartReader

import json

import codecs

# api_key = '05167372f6ac3b2c618e55b0931660df36a7b6e9'
# dart=OpenDartReader(api_key)
#
# # list=~~~~~
#
#               # 005930: 삼성전자 코드
# res=dart.finstate('삼성전자', 2020, reprt_code='11013')
# print(res)
# print(res.info())

# https://opendart.fss.or.kr/api/fnlttSinglAcntAll.json?crtfc_key=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx&corp_code=00126380&bsns_year=2018&reprt_code=11011&fs_div=OFS


from bs4 import BeautifulSoup
# beutifulsoup 포기~~
# def get_craw(gcode='A035420'):
#     url = "http://comp.fnguide.com/SVO2/ASP/SVD_Finance.asp?NewMenuID=103&gicode="+gcode
#     res = requests.get(url)
#
#     soup = BeautifulSoup(res.text, "html.parser", )
#     # #divSonikY > table > tbody > tr:nth-child(1) 이게 첫번째 거라 >tr까지만 가져오면 된다
#
#     box_list = soup.select("#divSonikY > table > tbody > tr")
#
#     tot_list = []
#     for box in box_list:
#         list=[]
#         price1 = box.select_one("").text
#         price2 = box.select_one("").text
#
#         list.append(price1)
#         list.append(price2)
#
#         tot_list.append(list)
#
#         # 프레임 만드는 게 주 목적이면 df=pd.DataFrame(data=tot_list) 하고 return df
#         df=pd.DataFrame(data=tot_list)
#         return tot_list # [[],[],[]]
#
# df=get_craw(gcode='A035420')
# print(df.head())

####################################################################

def get_craw(gcode='A035420'):

    # ----------------------------------------------------
    # 네이버증권사에서 기업 리스트 원시적으로 텍스트로 가지고 있다
    # 이렇게 안 하고 fin 어쩌고 해도 되는데 이게 좀더 정확 따끈따끈한 재무정보라(?)
    # ----------------------------------------------------

    url = "http://comp.fnguide.com/XML/Market/CompanyList.txt"
    com_res = requests.get(url)

    print(com_res.encoding) # ISO-8859-1
    com_res.encoding = "utf-8-sig" # 그냥 utf-8하면 에러 날 수도 있다
    com_json = json.loads(com_res.text) # { "Co": [ {},{},{} ] }
    # print(com_res.text)
    # print(com_json["Co"])

    com_df=pd.DataFrame(data=com_json["Co"])
    # print(com_df.head())

    # Series.str.contains 외에도 start_with, end_with 등등 있다
    print(com_df[com_df['nm'].str.contains('카카오')][['cd', 'nm']])
    print(com_df[com_df['nm'].str.contains('카카오')]['cd'].tolist())


    url = f"http://comp.fnguide.com/SVO2/ASP/SVD_Finance.asp?NewMenuID=103&gicode={gcode}"
    headers={'User-Agent':'Mozilla'}

    res=requests.get(url, headers=headers)
    soup=BeautifulSoup(res.text, "html.parser")
    img1=soup.select_one("#sonikChart1").get("src")  # 손익계산서(주요재무항목)
    img2=soup.select_one("#sonikChart2").get("src")  # 손익계산서(성장송지표)
    img3=soup.select_one("#deachaChart1").get("src") # 재무상태표(주요재무항목)
    img4=soup.select_one("#deachaChart2").get("src") # 재무상태표(안정성지표)
    img5=soup.select_one("#cashChart1").get("src")   # 현금흐름표(Invested Capital)
    img6=soup.select_one("#cashChart1").get("src")   #현금흐름표(Free Cash Flow)
    img_list=[img1, img2, img3, img4, img5, img6]
    print(img_list)

    table_list = pd.read_html(url, encoding='UTF-8')
    print(len(table_list))

    print(table_list[0].info())
    print(table_list[0].head())

    # tot_list = []
    # print(box_list)
    #
    # for box in box_list:
    #     print(box)
    #     for item in box:
    #         title = box.select_one('th > div').text
    #         print(item)
        # list=[]
        # price1 = box.select_one("th > div").text
        # price2 = box.select_one("").text
        #
        # list.append(price1)
        # list.append(price2)
        #
        # tot_list.append(list)

        # 프레임 만드는 게 주 목적이면 df=pd.DataFrame(data=tot_list) 하고 return df
        # df = pd.DataFrame(data=tot_list)
        # return tot_list  # [[],[],[]]


get_craw(gcode='A035420')