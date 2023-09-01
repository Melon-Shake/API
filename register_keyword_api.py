import streamlit as st
import requests
import psycopg2
import bcrypt
import melon_config
from pydantic import BaseModel
from fastapi import FastAPI
from datetime import datetime
from config import db_params
from typing import Optional

#from multistate_page import MultiPage
class LoginData(BaseModel):
    email : str
    password : str
    gender : str
    birthdate: str
    mbti : str
    favorite_tracks : str
    favorite_artists : str
    name : str

api = FastAPI()

@api.post("/get_user_data/") 
def get_user_data(data: LoginData):
    email = data.email
    password = data.password
    gender = data.gender

    birthdate = datetime.strptime(data.birthdate, "%Y%m%d")
    today = datetime.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

    mbti = data.mbti
    favorite_tracks = data.favorite_tracks
    favorite_artists = data.favorite_artists
    name = data.name
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()
    # 패스워드 해싱
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    # INSERT 쿼리 실행
    user_query = "INSERT INTO \"user\"(password,email,name) values (%s, %s,%s) RETURNING id;"
    user_values = (hashed_password,email,name)
    cursor.execute(user_query, user_values)
    user_detail_query = "INSERT INTO user_properties(gender,age,mbti,favorite_tracks,favorite_artists,user_id) values (%s,%s,%s,%s,%s,%s)"

    #try:
        
    user_query_id = cursor.fetchone()[0]
    user_detail_values= (gender,age,mbti,favorite_tracks,favorite_artists,user_query_id)
    cursor.execute(user_detail_query,user_detail_values)
    connection.commit()
    cursor.close()
    connection.close()
    #    st.write("등록이 완료되었습니다.")
    #except psycopg2.IntegrityError as e:
    #    st.write("이미 등록된 ID입니다.")

class Keyword(BaseModel):
    keyword: str
    email: str  # 사용자 이메일
@api.post("/get_keyword_data/") 
def get_keyword_data(data: Keyword):
    keyword = data.keyword
    email = data.email  # 사용자 이메일

    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()

    # 등록한 이메일인 경우 ID 가져오기
    user_query = "SELECT id FROM \"user\" WHERE email = %s;"
    user_values = (email,)
    cursor.execute(user_query, user_values)
    user_query_result = cursor.fetchone()

    if user_query_result:
        user_id = user_query_result[0]
    else:
        user_id = None

    search_query = "INSERT INTO search_log_keywords(keyword,user_id) values (%s,%s);"
    user_values = (keyword, user_id)
    cursor.execute(search_query, user_values)

    connection.commit()
    cursor.close()
    connection.close()
