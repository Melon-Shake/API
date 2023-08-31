from fastapi import FastAPI
import requests
import module
from pydantic import BaseModel
import bcrypt
import psycopg2
from datetime import datetime
from config.db_info import db_params

app = FastAPI()

access_token = module.read_AuthToken_from_file()

class LoginData(BaseModel):
    email : str
    password : str
    gender : str
    birthdate: str
    mbti : str
    favorite_tracks : str
    favorite_artists : str
    name : str

class SearchKeyword(BaseModel):
    searchInput : str

@app.post("/search/")
def search_spotify(data:SearchKeyword):
    q = data.searchInput
    url = f'https://api.spotify.com/v1/search?q={q}&type=album%2Cartist%2Ctrack&market=kr'
    headers = {
        'Authorization': 'Bearer '+access_token
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        return_data ={}
        for i in range(len(response_json["tracks"]["items"])):
            list_artist = []
            for j in range(len(response_json["tracks"]["items"][i]["artists"])):
                list_artist.append(response_json["tracks"]["items"][i]["artists"][j]["name"])
            return_data["tracks"+str(i)]=[[response_json["tracks"]["items"][i]["name"]],
                            [response_json["tracks"]["items"][i]["album"]["name"]],
                            list_artist]                
        # for i in range(len(response_json["albums"]["items"])):
        #     # print(response_json["albums"]["items"][i]["name"])
        #     return_data["albums"+str(i)]=[[response_json["albums"]["items"][i]["name"]]]
        # for i in range(len(response_json["artists"]["items"])):
        #     # print(response_json["artists"]["items"][i]["name"])
        #     return_data["artists"+str(i)]=[[response_json["artists"]["items"][i]["name"]]]
            # response_json["tracks"]["items"]["name"]
        # print(len(response_json))
        print(return_data)
        return return_data
    else:
        return {"error": "Spotify API request failed"}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)

# junsung
@app.post("/get_user_data/")
def get_user_data(data: LoginData):
    email = data.email
    password = data.password
    gender = data.gender
    birthdate = datetime.strptime(data.birthdate, "%Y-%m-%d")
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
    try:
        user_query = "INSERT INTO \"user\"(password,email,name) values (%s, %s,%s) RETURNING id;"
        user_values = (hashed_password,email,name)
        cursor.execute(user_query, user_values)
        user_detail_query = "INSERT INTO user_properties(gender,age,mbti,favorite_tracks,favorite_artists,user_id) values (%s,%s,%s,%s,%s,%s)"
        user_query_id = cursor.fetchone()[0]
        user_detail_values= (gender,age,mbti,favorite_tracks,favorite_artists,user_query_id)
        cursor.execute(user_detail_query,user_detail_values)
        connection.commit()
        cursor.close()
        connection.close()
    except (psycopg2.IntegrityError, psycopg2.Error) as e:
        if "duplicate key value violates unique constraint" in str(e):
            # print("이미 등록된 Email 입니다.")
            return "이미 등록된 Email 입니다."
        else:
            # print("다른 예외 발생:", e)
            return "다른 예외 발생"
class Keyword(BaseModel):
    searchInput: str
    email: str  # 사용자 이메일
@app.post("/get_keyword_data/")
def get_keyword_data(data: Keyword):
    keyword = data.searchInput
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