import cx_Oracle as cx
import pandas as pd

"""`
미션 1: 리스트의 리스트로 담기
"""

emp_list=[]

# ----------cx oracle
conn = cx.connect("ai", "1111", "127.0.0.1:1521/XE")
cur = conn.cursor()

# ---------- sql문
sql = f"select empno, ename,sal, hiredate, job, deptno from emp"

# ---------- sql문 실행
cur.execute(sql)

for c in cur:
    emp_list.append(list(c))
cur.close()
conn.close()

print(emp_list)

"""`
미션 2: 리스트에 dic로 담기
"""

emp_list=[]

# ----------cx oracle
conn = cx.connect("ai", "1111", "127.0.0.1:1521/XE")
cur = conn.cursor()

# ---------- sql문
sql = f"select empno, ename,sal, hiredate, job, deptno from emp"

# ---------- sql문 실행
cur.execute(sql)

for c in cur:
    row_dict={}
    for i, col in enumerate(['empno', 'ename','sal', 'hiredate', 'job', 'deptno']):
        row_dict[col]=c[i]
    emp_list.append(row_dict)
cur.close() ### close 무조건 해라!!
conn.close() ### close 무조건 해라!!

print(emp_list)

###########강사님 수업 부분

# 예전에 excutemany 도 했었다.(list의 list 형태)
# def test_insert(list):
#     conn = cx.connect("ai", "0000", "localhost:1521/XE")
#     cur = conn.cursor()
#     sql = "insert into test2 values(:1,:2, :3)"
#     cur.executemany(sql, list)
#     cur.close()
#     conn.commit()
#     conn.close()
# list = [[3,'aa',date.fromisoformat('2022-01-01')],
#         [4,'bb',date.fromisoformat('2022-01-02')]
#        ]
# test_insert(list)

# 데이터 프레임 것을 list의 list로 불러오는 방법
# df.values.tolist()

# close 무조건 해라!! 안 그러면 데이터 눕는다 -> with문법 추천
# 오라클에 datetime.datetime 안 들어가니까 변경하는 법 확인해보기
# dict에서 key에 'data'해서 value를 리스트로 통으로 넣는 방법도 쓸 수 있다.

#=================================================
# 방법2) pandas 사용
#=================================================

# 통으로 불러오기
# conn=cx.connect("ai", "0000", "localhost:1521/XE")
# sql="select empno, ename,sal, hiredate, job, deptno from emp"
# df=pd.read_squl(sql, conn) # read_sql문 안에 있는 게 위에서 한 dict 한 그 구조
# print(df.head())
#
# # 리스트의 리스트로 가져와서 주기
# print(df.values.tolist()) # ---------[ [ ] , [  ], ..]
#
# # 리스트의 딕트로 가져와서 주기
# print(df.to_dict()) # ---------{ 'col': {'row1':   , 'row2':    }, 'col2' 이런 식
# print(df.to_dict('split')) # pandas api 참고
# print(df.to_dict('index')) # index가 key가 되고 안에 col별 데이터 딕트로 들어감

#=================================================
# 방법2) sql.alchemy 사용 - ORM (Django 관련)쓰면 필수!!!!
#=================================================
# import sqlalchemy # lec_11_oracle_All 참고 연결문법이 많이 다르다 나머지는 쓰던 방법대로
# ORM 은 뭐고 왜 쓰나요
# object relation map -> sql 에서 가져온 컬럼을 자동으로 python에 담아주자. object는 클래스에 있는 걸 의미

# # ================================================
# # ================================================
# # insert 하기
# # ================================================
# # ================================================
#
# # 뽑아낸 list의 list를 insert해라
#
# # ====================================
# # 미션 1: 리스트 하나
# # ====================================
# get_list = [9999, 'AAAA', 800.0, '1980-12-17', 'CLERK', 20]
# conn = cx.connect("ai", "1111", "127.0.0.1:1521/XE")
#
# sql = """insert
#         into empcp(empno, ename,sal, hiredate, job, deptno)
#         values(:1, :2, :3, to_date(:4, 'YYYY-MM-DD'), :5, :6) """
# cur=conn.cursor()
# cur.execute(sql, get_list)
# cur.close()
# conn.commit()
# conn.close()
#
#
# # ====================================
# # 미션2 : list의 list
# # ====================================
# import datetime
#
# get_list=[[7369, 'SMITH', 800.0, datetime.datetime(1980, 12, 17, 0, 0), 'CLERK', 20], [7499, 'ALLEN', 1600.0, datetime.datetime(1981, 2, 20, 0, 0), 'SALESMAN', 30], [7521, 'WARD', 1250.0, datetime.datetime(1981, 2, 22, 0, 0), 'SALESMAN', 30], [7566, 'JONES', 2975.0, datetime.datetime(1981, 4, 2, 0, 0), 'MANAGER', 20], [7654, 'MARTIN', 1250.0, datetime.datetime(1981, 9, 28, 0, 0), 'SALESMAN', 30], [7698, 'BLAKE', 2850.0, datetime.datetime(1981, 5, 1, 0, 0), 'MANAGER', 30], [7782, 'CLARK', 2450.0, datetime.datetime(1981, 6, 9, 0, 0), 'MANAGER', 10], [7788, 'SCOTT', 3000.0, datetime.datetime(1987, 7, 13, 0, 0), 'ANALYST', 20], [7839, 'KING', 5000.0, datetime.datetime(1981, 11, 17, 0, 0), 'PRESIDENT', 10], [7844, 'TURNER', 1500.0, datetime.datetime(1981, 9, 8, 0, 0), 'SALESMAN', 30], [7876, 'ADAMS', 1100.0, datetime.datetime(1987, 7, 13, 0, 0), 'CLERK', 20], [7900, 'JAMES', 950.0, datetime.datetime(1981, 12, 3, 0, 0), 'CLERK', 30], [7902, 'FORD', 3000.0, datetime.datetime(1981, 12, 3, 0, 0), 'ANALYST', 20], [7934, 'MILLER', 1300.0, datetime.datetime(1982, 1, 23, 0, 0), 'CLERK', 10]]
# for list in get_list:
#     list[3]=str(list[3])  #슬라이싱으로 연월일만 뽑고 to_date(:4, 'YYYY-MM-DD') 해도 되겠다.
#
# conn = cx.connect("ai", "1111", "127.0.0.1:1521/XE")
#
# sql = """insert
#         into empcp(empno, ename,sal, hiredate, job, deptno)
#         values(:1, :2, :3, to_date(:4, 'YYYY-MM-DD HH24:MI:SS'), :5, :6) """
# cur=conn.cursor()
# cur.executemany(sql, get_list)
# cur.close()
# conn.commit()
# conn.close()
#
# # ====================================
# # 강사님
# # ====================================
# 주의: sql development 랑 파이썬 둘 다 열었을 때는 꼭 양쪽에서 commit해주기
# str -> date처리
# from datetime import datetime, date
# 방법 1: [111, 'kim', datetime.strptime('2020/07/18', '%Y/%m/%d')]
# 방법 2: [111, 'kim', datetime.fromisoformat('2020/07/18')]
# 방법 3: 아예 오라클 sql문법에서 to_date(:3, 'YYYY-MM-DD')

# # ====================================
# 방법2) pandas 사용 : to_sql 해야 됨

# df 준비
conn = cx.connect("ai", "1111", "127.0.0.1:1521/XE")
cur=conn.cursor()

sql = "select empno, ename,sal, hiredate, job, deptno from emp where deptno=10"
emp_df=pd.read_sql(sql, conn)
print(emp_df.head())
print(emp_df.values.tolist())



# to_sql로 해보자 -> create table 안 해도 됨

# 기존처럼 하면 오라클 안 먹는다 -> sqlalchemy 해야됨
# cur.executemany(sql, get_list)
# cur.close()
# conn.commit()
#
# conn.close()
# res=emp_df.to_sql("empcp33", conn, # schema=None(컬럼 이름 별도로 지정하고 싶으면)
#               index=False, # index_label: 인덱스 레이블 True일 때
#                             # chuncksize 값 주면 해당 값만큼 잘러서 넣고 지정 안 하면 통째로 구겨넣음
#                             # dtype 하나 하나 지정하고 싶으면
#               if_exists='fail' # replace, append
#               )
# print(res)

import sqlalchemy as sa
engine = sa.create_engine('oracle://ai:1111@localhost:1521/XE')
conn = engine.connect()

res=emp_df.to_sql("empcp33", conn, # schema=None(컬럼 이름 별도로 지정하고 싶으면)
              index=False, # index_label: 인덱스 레이블 True일 때
                            # chuncksize 값 주면 해당 값만큼 잘러서 넣고 지정 안 하면 통째로 구겨넣음
                            # dtype 하나 하나 지정하고 싶으면
              if_exists='fail' # replace(에러), append(된다)
              )
print(res)



# insert list의 list도 가능 -> 문법 제대로 안 돼있다.

# sql = """insert
#         into empcp(empno, ename,sal, hiredate, job, deptno)
#         values(:1, :2, :3, to_date(:4, 'YYYY-MM-DD HH24:MI:SS'), :5, :6) """
# cur=conn.cursor()
# cur.executemany(sql, get_list)
# cur=conn.cursor()
# # cur.executemany(sql, get_list)
# # cur.close()
# # conn.commit()
# # conn.close()

