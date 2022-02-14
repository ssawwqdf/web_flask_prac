from flask import Flask, make_response, jsonify, request, render_template
import cx_Oracle

app = Flask(__name__) #, template_folder="", static_folder="") # 플라스크 클래스에서 구동되는 것 생성자에 넣는다.
                        # app이란 이름으로 flask 구동할 때 관리하겠다.



@app.route('/')
def index():
    mylist=[1,2,3]
    point = 10000

    sql = "select empno, ename,sal, hiredate, job, deptno from emp"

    return render_template("index.html",
                           MY_LIST=mylist,
                           MY_POINT=point)


def hello():
    # return 'Hello World!'
    return render_template("index.html")

@app.route('/123')
def hello123():
    return '123412341234'

if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0', port=80)