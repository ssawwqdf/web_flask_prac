from flask import Flask, make_response, jsonify, request, render_template
import cx_Oracle

import sqlalchemy as sa
import pandas as pd

import json

app = Flask(__name__) #, template_folder="", static_folder="") # 플라스크 클래스에서 구동되는 것 생성자에 넣는다.
                        # app이란 이름으로 flask 구동할 때 관리하겠다.
@app.route('/')      # 웹 주소 뒤에 뭐 들어오면 아래 거 실행한다
def index():

    return render_template("ajax_test.html") # 로그인 하게 만들어놓음 (DB에서 실제 회원 있나 찾게 만들 수 있다.)


@app.route('/form_submit_post', methods=["post"])      # 웹 주소 뒤에 뭐 들어오면 아래 거 실행한다, methods는 ["post", "get"] 둘 다 써도 되고 하나만 써도 되고
                                                # post method로 요청 들어오면 아래 내용 실행
def form_submit_post():
    # 웹페이지 <form>에서 넘어온 값 http://192.168.0.5:9999/form_submit_post
    userid=request.form.get("userid") # name="userid"
    userpw=request.form.get("userpw")  # name="userpw"
    print("form_submit post ...........실행", userid, userpw)

    return render_template("ajax_test_result.html", MY_MSG="ok") # 추가로 값 주고 싶으면


@app.route('/form_submit_get', methods=["get"])  # 웹 주소 뒤에 뭐 들어오면 아래 거 실행한다, methods는 ["post", "get"] 둘 다 써도 되고 하나만 써도 되고
# post method로 요청 들어오면 아래 내용 실행
def form_submit_get(): # 주소는 같아도 되는데 함수 이름은 같으면 안 됨!!!!!!!!!
    # 웹페이지 <form>에서 넘어온 값 http://192.168.0.5:9999/form_submit_get?userid=%EA%B8%B0%EB%B3%B8%EC%95%84%EC%9D%B4%EB%94%94&userpw=asdf
    # get은 ? 뒤에 있는 쿼리스트링 즉 아규먼트를 표시한다

    userid = request.args.get("userid")  # name="userid" / requests아니고 request임 이건 flask에서 주는 거
    userpw = request.args.get("userpw")  # name="userpw"

    # select ~~~~from ~~~ where :1, :2 하고 execute 하면 sql에 있는 것도 불러올 수 있다!!

    print("form_submit get ...........실행", userid, userpw)

    return render_template("ajax_test_result.html", MY_MSG="ok")  # 추가로 값 주고 싶으면

@app.route('/form_ajax', methods=["post"])  # 웹 주소 뒤에 뭐 들어오면 아래 거 실행한다, methods는 ["post", "get"] 둘 다 써도 되고 하나만 써도 되고
# post method로 요청 들어오면 아래 내용 실행
def form_ajax():
    # 웹페이지 <form>에서 넘어온 값 json 형태로 받는다
    data=request.get_data() # get_json으로 하면 근데 안 되고 get_data로 해서 받아온다
    print("form_submit ajax ...........실행", data)
    # return "ok" # 비동기는 휙휙 바뀌는 게 아니라 그냥 값만 주면 된다

    # list=[["smith", 1400],
    #       ["allen", 4000] # db 갔다왔다 치고 list의 list 만들어보자
    #       ]
    list = [{"ename": "smith", "sal": 1400},
            {"ename": "allen", "sal": 4000}
            ]

    list_str=json.dumps(list) # csv -> df (load)니까 list -> str은 dumps (s 안 붙은 dump는 filepoint필요한데 이거 뭔지 모른다)

    return list_str


if __name__ == '__main__':               # 이 py 안에서 실행하면 '__main__'
    app.debug=True                       # 개발 끝나면 반드시 막아라
    app.run(host='0.0.0.0', port=9999)     # 포트번호는 웬만하면 5000 이상 아무거나 / 두 개 동시 띄울 때 포트 번호 같으면 누울 수도