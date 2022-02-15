import pandas as pd
# from flask_cors import CORS
from flask import Flask, jsonify


datas = [[1,2,3],
         [10,20,30],
         ]
df = pd.DataFrame(data=datas,
             columns=["a","b","c"]
             #dtype={"a":'int64', "b":'int64', "c":'object' }
             )
print(df.head())


datas = [ {"a":1,  "b":2,  "c":3},
          {"a":10, "b":20, "c":30}
        ]
df = pd.DataFrame(data=datas
             #dtype={"a":'int64', "b":'int64', "c":'object' }
             )
print(df.head())


import json # javascript object notation

list=df.values.tolist()
print(type(list), list, list[:1])     # 이게 진짜 리스트 / 객체로 꺼내고 싶으면 이렇게 써라

json_str = df.to_json(orient="values") # 값만 꺼내서 json 형태로 바꿔줘. ㅇㅇㅇ은 키가 되고 내용이 벨류가 된다.
print(type(json_str), json_str, json_str[:1])   #<class 'str'> [[1,2,3],[10,20,30]] -> 리스트의 리스트꼴 같지만 사실 스트링이라 [:1]하면 [ 만 꺼내진다

json_obj = json.loads(json_str)        # 객체가 아니라 str으로 왔을 때 객체로 바꾸고 싶으면  json.loads()해야한다.
print(type(json_obj),json_obj,  json_obj[:1])      #<class 'list'> [[1, 2, 3], [10, 20, 30]]

json_str = json.dumps(json_obj)
print(type(json_str),json_str,  json_str[:1])      #<class 'str'> [[1, 2, 3], [10, 20, 30]]

# json_list = jsonify(json_str)
# print(json_list)



# dict= {"id": 'kim', "pw":123}
# print(dict)
# dict["id"] = 'lee'
# print(dict)
dict= {}
dict["addr"] = '서울'
dict["pw"] = '111'
print(dict)
