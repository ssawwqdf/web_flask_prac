import pandas as pd
import numpy as np
from datetime import datetime, date
from bs4 import BeautifulSoup # 클래스라 생성자 만들어야 함

soup=BeautifulSoup()

# import cx_Oracle as cx
# conn = cx.connect("ai", "1111", "127.0.0.1:1521/XE")

import sqlalchemy as sa
engine = sa.create_engine('oracle://ai:1111@localhost:1521/XE')
conn = engine.connect()

import requests

url="http://www.realmeter.net/category/politics/"
# 주소에 ? 있다 -> get  방식 써라
# 파라미터 직접 빼고 싶으면 dict로 만들거나 해서 params에 넘기면 된다
# params=my_dict 해도 되고, **mydict 써도 됨(후자 방식 주로 쓴다.)

res=requests.get(url)  #, params=None) # 주소에서 ? 뒷 부분이 params
# print(res)
# print(res.text)

soup=BeautifulSoup(res.text, 'html.parser')
# soup.select_one() # 하나만 꺼내줘
# soup.select() # for문에 넣으면 반복적으로 가져온다

res = requests.get(url)
# print(res)
# print(res.text)

#

soup = BeautifulSoup(res.text,  "html.parser", )
box_list = soup.select("body > div > div.main.wrap.cf > div > div > div.posts-list.listing-alt > article")
# # 네모박스 여러개를 가져와줘 -> loop 돌려야 됨 / 괄호 안에 가져온 소스 넣으면 된다

# 가져오기
# for box in box_list:                          # box_list에 아티클 부분까지 들어있어서 그 안에 있는 거 가져오려면 그 부분 생략하면 도니다
#     rdate = box.select_one("div > time").text # 텍스트 부분만 가져올 거면 .text 붙이면 된다
#     title = box.select_one("div > a").text
#     href  = box.select_one("div > a").get("href") # 태그에 있는 거 가져올 거면 get 하고 태그 이름
#     content = box.select_one("div > div > p").text
#     pic = box.select_one("a > img").get("src")
#
#     print(rdate, title, href, content, pic)

# DB에 넣어보자
tot_list=[]
for box in box_list:                          # box_list에 아티클 부분까지 들어있어서 그 안에 있는 거 가져오려면 그 부분 생략하면 도니다
    rdate = box.select_one("div > time").text # 텍스트 부분만 가져올 거면 .text 붙이면 된다
    title = box.select_one("div > a").text
    href  = box.select_one("div > a").get("href") # 태그에 있는 거 가져올 거면 get 하고 태그 이름
    content = box.select_one("div > div > p").text
    pic = box.select_one("a > img").get("src")
    df_list=[rdate, title, href, content, pic]
    tot_list.append(df_list)
tot_arr=np.array(tot_list)
df=pd.DataFrame(tot_arr, columns=['rdate', 'title', 'href', 'content', 'pic'])
print(df)

# df.to_sql("pres_elec", conn,
#                if_exists='fail', # append:된다 _________ replace:에러
#                index=False,      # index=True,index_label=None,
#                                  # chunksize=None,
#                                  # dtype=None, method=None
#                                  #schema=None
#              )

    # print(rdate, title, href, content, pic)