from fastapi import FastAPI, HTTPException
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
import requests
from model.chart_genie import ChartGenieORM
from model.chart_flo import ChartFloORM
from model.chart_vibe import  VibeORM
from model.chart_bugs import  BugsORM
from model.chart_melon import MelonORM
from typing import Dict, List, Union
from model.database import session_scope
import requests
from model.jun_model import *
from get_keyword import save_keyword_data
from user_data import user_data
from user_search_track import pick_data
from daily_search_ranking import daily_search_ranking
# import sys, numpy as np, pandas as pd, json, requests, re



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
        return return_data
    else:
        return {"error": "Spotify API request failed"}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)

# junsung login api
@app.post("/get_user_data/")
def get_user_data(data: LoginData):
   user_data(data, db_params)
    
@app.post("/get_keyword_data/")
def get_keyword_data(data: Keyword): 
    save_keyword_data(data, db_params)


@app.post("/get_use_data/")
def get_use_data(data: search_track):
    pick_data(data,db_params)
    
    

@app.post("/daily_search_ranking/")
def get_daily_search_ranking():
    search_ranking_result = daily_search_ranking()
    return search_ranking_result

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

# chart api
@app.post("/chart/integrated_chart/")
def get_integrated_chart():
    class TotalChart(BaseModel) :
        track_name : str
        artist_name : str
        album_name : str
        points : Union[int, float]
        
    with session_scope() as session:
        genieOrms = session.query(ChartGenieORM).all()
        VibeOrms = session.query(VibeORM).all()
        floOrms = session.query(ChartFloORM).all()
        bugsOrms = session.query(BugsORM).all()
        melonOrms = session.query(MelonORM).all()

    entrie_genie = [ TotalChart(
                    track_name=genieOrm.song_name
                    ,artist_name=genieOrm.artist_name
                    ,album_name=genieOrm.album_name
                    ,points=genieOrm.points
                ) for genieOrm in genieOrms]
    
    entrie_vibe = [ TotalChart(
                    track_name=VibeOrm.track_title
                    ,artist_name=VibeOrm.artist_name
                    ,album_name=VibeOrm.album_title
                    ,points=VibeOrm.points
                ) for VibeOrm in VibeOrms]

    entrie_flo = [ TotalChart(
                    track_name=floOrm.track_name,
                    artist_name=floOrm.artist_name,
                    album_name=floOrm.album_name,
                    points=floOrm.points
                    ) for floOrm in floOrms 
                  ]

    entrie_bugs = [ TotalChart(
                        track_name=bugsOrm.track_title
                        ,artist_name=bugsOrm.artist_name
                        ,album_name=bugsOrm.album_title
                        ,points=bugsOrm.points
                    ) for bugsOrm in bugsOrms]
    
    entrie_melon = [ TotalChart(
                    track_name=melonOrm.song_name
                    ,artist_name=melonOrm.artist_name
                    ,album_name=melonOrm.album_name
                    ,points=melonOrm.points
                ) for melonOrm in melonOrms]
    
    integrated = []
    integrated.extend(entrie_bugs)
    integrated.extend(entrie_flo)
    integrated.extend(entrie_genie)
    integrated.extend(entrie_vibe)
    integrated.extend(entrie_melon)
    
    merged_df = pd.DataFrame([vars(chart) for chart in integrated])
    merged_df = merged_df.apply(lambda x: x.str.replace(r'\s+', '', regex=True) if x.dtype == "object" else x)
    merged_df['track_name'] = merged_df['track_name'].str.replace("’", "'")
    # merged_df['track_name'] = merged_df['track_name'].str.replace("'", "")
    merged_df['track_name'] = merged_df['track_name'].str.lower()
    merged_df['artist_name'] = merged_df['artist_name'].str.lower()
    result_df = merged_df.groupby(['track_name', 'artist_name', 'album_name'])['points'].sum().reset_index()
    result_df = merged_df.groupby(['track_name', 'artist_name'])['points'].sum().reset_index()
    result_df = result_df.sort_values(by='points', ascending=False).reset_index()
    
    df = result_df.drop('index', axis=1)
    json_string = df.to_json(orient='records', lines=True, default_handler=str, force_ascii=False)
    return(json_string)

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
