from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import requests
import sys
import os
root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(root_path)
import lib.module as module
from pydantic import BaseModel
import bcrypt
import psycopg2
from datetime import datetime
from config.db_info import db_params
from lyric import lyric_search_and_input
from sp_track import sp_and_track_input, get_sp_track_id
from update_token import return_token
# import sys, numpy as np, pandas as pd, json, requests, re
import requests
import sys
import os
root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(root_path)

app = FastAPI()

# access_token = module.read_AuthToken_from_file()

_APP_VERSION = "6.5.8.1"
_CP_ID = "AS40"
_USER_AGENT = f"{_CP_ID}; Android 13; {_APP_VERSION}; sdk_gphone64_arm64"
_CHART_API_URL = f"https://m2.melon.com/m6/chart/ent/songChartList.json?cpId={_CP_ID}&cpKey=14LNC3&appVer={_APP_VERSION}"


class MelonChartRequestException(Exception):
    pass

class MelonChartParseException(Exception):
    pass

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
    
class lyric_data(BaseModel):
    artist : str
    track : str
    track_id : int
    GENIUS_API_KEY : str = "U1RN70QWau9zk3qi3BPn_A-q4Bft_3jnw8uLBp2lVafQgOQiA_kjSEyxzr88eI9d"

class sp_data(BaseModel):
    artist : str
    album : str
    track : str

# sophie api
@app.get('/token/')
def update_token():
    access_token = return_token()
    return access_token

# ssg search api
@app.post("/search/track/")
async def search_spotify(data:SearchKeyword):
    #***************** access_token = requests.get('http://0.0.0.0:8000/token')*****************
    access_token = return_token()
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
        print(return_data)
        return return_data
    else:
        return {"error": "Spotify API request failed"}
    
@app.post("/search/artist/")
async def search_spotify(data:SearchKeyword):
    #***************** access_token = requests.get('http://0.0.0.0:8000/token')*****************
    access_token = return_token()
    q = data.searchInput
    url = f'https://api.spotify.com/v1/search?q={q}&type=album%2Cartist%2Ctrack&market=kr'
    headers = {
        'Authorization': 'Bearer '+access_token
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        return_data ={}
        for i in range(len(response_json["artists"]["items"])):
            return_data["artists"+str(i)]=[[response_json["artists"]["items"][i]["name"]],
                                           [response_json["artists"]["items"][i]["genres"]],
                                           [response_json["artists"]["items"][i]["images"][0]["url"]]]
        print(return_data)
        return return_data
    else:
        return {"error": "Spotify API request failed"}

@app.post("/search/album/")
async def search_spotify(data:SearchKeyword):
    #***************** access_token = requests.get('http://0.0.0.0:8000/token')*****************
    access_token = return_token()
    q = data.searchInput
    url = f'https://api.spotify.com/v1/search?q={q}&type=album%2Cartist%2Ctrack&market=kr'
    headers = {
        'Authorization': 'Bearer '+access_token
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        return_data ={}              
        for i in range(len(response_json["albums"]["items"])):
            return_data["albums"+str(i)]=[[response_json["albums"]["items"][i]["name"]],
                                          [response_json["albums"]["items"][i]["images"][0]['url']],
                                          [response_json["albums"]["items"][i]["artists"]["name"]],
                                          [response_json["albums"]["items"][i]["release_date"]]]
        print(return_data)
        return return_data
    else:
        return {"error": "Spotify API request failed"}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)

# junsung login api
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
    user_query = "INSERT INTO \"user\"(password,email,name) values (%s, %s,%s) RETURNING id;"
    user_values = (hashed_password.decode("utf-8"),email,name)
    cursor.execute(user_query, user_values)
    user_detail_query = "INSERT INTO user_properties(gender,age,mbti,favorite_tracks,favorite_artists,user_id) values (%s,%s,%s,%s,%s,%s)"
    try:
        user_query_id = cursor.fetchone()[0]
        user_detail_values= (gender,age,mbti,favorite_tracks,favorite_artists,user_query_id)
        cursor.execute(user_detail_query,user_detail_values)
        connection.commit()
        cursor.close()
        connection.close()
    except (psycopg2.IntegrityError, psycopg2.Error) as e:
        if "duplicate key value violates unique constraint" in str(e):
            print("이미 등록된 Email 입니다.")
            return "이미 등록된 Email 입니다."
        else:
            print("다른 예외 발생:", e)
            return "다른 예외 발생"
class Login(BaseModel):
    email:str
    password:str

@app.post("/login/")
def login(login_data:Login):  
    email = login_data.email
    password = login_data.password
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()

    # 등록한 이메일인 경우 ID 가져오기
    user_query = "SELECT password FROM \"user\" WHERE email = %s;"
    user_values = (email,)
    cursor.execute(user_query, user_values)
    user_query_result = cursor.fetchone()

    if user_query_result:
        condition = bcrypt.checkpw(password.encode("utf-8"), user_query_result[0].encode("utf-8"))
        cursor.close()
        if condition:
                # 패스워드가 일치하면 로그인 성공
                return True
        else:
            return False
        
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

class search_track(BaseModel):
   email : str
   track_title : str
   
@app.post("/get_use_data/")
def get_use_data(data: search_track):
    email = data.email
    track_title = data.track_title

    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()
    
    user_query = "SELECT id FROM \"user\" WHERE email = %s;"
    user_values = (email,)
    cursor.execute(user_query, user_values)
    user_query_result = cursor.fetchone()
    if user_query_result:
        user_id = user_query_result[0]
    else:
        user_id = None

    track_search = "SELECT id from track where name_org = %s"
    track_value = (track_title,)
    cursor.execute(track_search, track_value)
    track_query_result = cursor.fetchone()
    if user_query_result:
        track_id = track_query_result[0]

    search_query = "INSERT INTO search_log_tracks(track_id,user_id) values (%s,%s);"
    user_values = (track_id, user_id)
    cursor.execute(search_query, user_values)
    connection.commit()
    cursor.close()
    connection.close()

@app.post("/daily_search_ranking/")
def get_daily_search_ranking():
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()

    search_query = """

          SELECT keyword, RANK() OVER (ORDER BY MAX(created_datetime) DESC, COUNT(*) DESC) AS search_rank
        FROM search_log_keywords
        GROUP BY keyword
        ORDER BY search_rank;

    """

    value_check_query = """
        SELECT item
        FROM (
            SELECT name_org as item FROM artist
            UNION ALL
            SELECT name_org as item FROM track
            UNION ALL
            SELECT name_org as item FROM album
        ) AS items
        WHERE item IS NOT NULL
        AND item = %s;
    """

    cursor.execute(search_query)
    search_ranking = cursor.fetchall()

    result = {}
    prev_search_rank = None
    rank = 0
    
    for _, (keyword, search_rank) in enumerate(search_ranking):
        cursor.execute(value_check_query, (keyword,))
        if cursor.fetchone():
            if search_rank != prev_search_rank:  # 동일한 순위가 아니면 순위 업데이트
                rank += 1
        result[rank] = keyword
        prev_search_rank = search_rank
            
        if rank >= 20:  # 20위까지만 결과 저장
            break
    
    connection.close()
    return result

# bkson chart api
@app.post("/chart/melon_chart/")
def get_melonChat():
    headers = {"User-Agent": _USER_AGENT}
    res = requests.get(_CHART_API_URL, headers=headers)
    data = res.json()

    ## 멜론차트_TOP100NOW
    page_name = data["response"]["PAGE"]
    
    ## 2023.08.31 15:00
    update_time = f"{data['response']['RANKDAY']} {data['response']['RANKHOUR']}"
    
    ## datetime.datetime(2023, 8, 31, 15, 0)
    date_format = "%Y.%m.%d %H:%M"
    pre_date = datetime.strptime(update_time, date_format)
    
    entries = {}
    song_list = data['response']['SONGLIST'] 

    for item in range(len(song_list)):
        song_name = song_list[item]['SONGNAME'] 
        artist = song_list[item]['ARTISTLIST'][0]['ARTISTNAME']
        image = song_list[item]['ALBUMIMG']
        # rank = song_list[item]['CURRANK']
        pastrank = song_list[item]['PASTRANK']
        isNew = song_list[item]['RANKTYPE'] == "NEW"

        entries[str(item+1)]= [song_name, artist, image, pastrank, isNew]

    return entries

# Lucete api
@app.post("/lyric_input/")
def lyric_input(item : lyric_data):
    artist = item.artist
    track = item.track
    track_id = item.track_id
    GENIUS_API_KEY = item.GENIUS_API_KEY
    
    result = lyric_search_and_input(artist,track,track_id,GENIUS_API_KEY)
    if result:
        return {"result" : f"Lyrics have been added to track_id : {track_id}"}
    else:
        raise HTTPException(status_code=404, detail="Lyric ERR.")
    
@app.post("/sp_and_track_update/")
def sp_track_input(item: sp_data):
    artist = item.artist
    album = item.album
    track = item.track
    d = get_sp_track_id(artist, album, track)
    
    if d[0] is not None and d[1] is not None:  # get_sp_track_id 함수의 반환값이 None이 아닌지 확인
        result = sp_and_track_input(d[0], d[1], artist, album, track)
        return result
    else:
        raise HTTPException(status_code=404, detail="Track not found or error in processing.")

