from flask import Flask, make_response, jsonify, request, render_template
import cx_Oracle

import sqlalchemy as sa
import pandas as pd

import json

import requests
from bs4 import BeautifulSoup

from flask_cors import CORS, cross_origin

# ------------------------------------
#pip install flask_cors
# import flask_cors CORS, cross_origin
# CORS(app)
# CORS(app, resources={r'*': {'origins': '*'}})
# ------------------------------------

app = Flask(__name__) #, template_folder="", static_folder="") # 플라스크 클래스에서 구동되는 것 생성자에 넣는다.
                        # app이란 이름으로 flask 구동할 때 관리하겠다.
CORS(app) # cross domain 하려고

# ---------------강사님 코드 가져옴
def my_news_realmeter():
    # to_sql(table_name, sqlalchemy.conn만가능)
    engine = sa.create_engine('oracle://ai:1111@localhost:1521/XE')
    conn = engine.connect()

    url = "http://www.realmeter.net/category/politics/"
    res = requests.get(url)

    soup = BeautifulSoup(res.text, "html.parser", )
    box_list = soup.select("body > div > div.main.wrap.cf > div > div > div.posts-list.listing-alt > article")

    # ----------------------------------------------------list[list]
    tot_list = []
    for box in box_list:
        list = []
        rdate = box.select_one("div > time").text
        title = box.select_one("div > a").text
        href = box.select_one("div > a").get("href")
        content = box.select_one("div > div > p").text
        pic = box.select_one("a > img").get("src")
        list.append(rdate)
        list.append(title)
        list.append(href)
        list.append(content)
        list.append(pic)
        tot_list.append(list)

    df = pd.DataFrame(data=tot_list,
                      columns=["rdate", "title", "href", "content", "pic"]
                      # dtype={"a":'int64', "b":'int64', "c":'object' }
                      )
    # 자동으로 테이블을 만들어 준다. 단.. 기존에 만들어져 있으면 에러가 난다.
    df.to_sql("pres_elec", conn)  # if_exists: str = "fail"
    print("=============done======", len(tot_list))



@app.route('/')      # 웹 주소 뒤에 뭐 들어오면 아래 거 실행한다
def index():
    mylist=[1,2,3]
    point = 10000

    engine = sa.create_engine('oracle://ai:1111@localhost:1521/XE')
    conn = engine.connect()
    df = pd.read_sql("select * from pres_elec", conn)
    html = df.to_html()

    json_list = df.to_json(orient="values")

    json_obj = json.loads(json_list)
    # str_json = json.dumps(json_obj)
    return render_template("index.html",
                           MY_NEWS=json_obj)


def hello():
    # return 'Hello World!'
    return render_template("index.html")

# -------------- 업체 이름 타이핑 할 때마다 실시간 비동기로 업체 명단 가져와서 return ---------------
@app.route('/com_search_ajax', methods=['post'])
def com_search_ajax():
    search_keyword= "카카오"

    # -------연습_DART open API.py에서 가져옴
    # flask에서 다른 사이트 거 가져오면 에러날 수도 있다.(jquery에서 crossDomain:true 했음에도 불구하고)
    # CORS(호출, 결과 주는 둘 사이의 도메인이 다른데 비동기 통신을 할 경우 발생하는 에러)
    # pip install flask_cors
    # 네이버는 비동기 막아놨다
    url = "http://comp.fnguide.com/XML/Market/CompanyList.txt"

    com_res = requests.get(url)
    com_res.encoding = "utf-8-sig"  # 그냥 utf-8하면 에러 날 수도 있다
    com_json = json.loads(com_res.text)  # { "Co": [ {},{},{} ] }
    com_df = pd.DataFrame(data=com_json["Co"])

    # --------- 웹에서 입력한 검색어와 관련된 업체만 가져오기 -----------
    # search_keyword = request.form.get["search_input"]
    temp=com_df[com_df['nm'].str.contains(search_keyword)][['cd', 'nm']].head()
    # print(temp.values.tolist()) # valuesㅇ 안 해도 list로 바꿔주긴 한다 -> return은 글자로 줘야됨

    return json.dumps(temp.values.tolist())

if __name__ == '__main__':               # 이 py 안에서 실행하면 '__main__'
    app.debug=True                       # 개발 끝나면 반드시 막아라
    app.run(host='0.0.0.0', port=80)     # 포트번호는 웬만하면 5000 이상 아무거나