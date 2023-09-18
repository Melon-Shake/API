from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import sys
import os
root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(root_path)
import pandas as pd
import lib.module as module
from pydantic import BaseModel
import bcrypt
import psycopg2
from datetime import datetime
from config.db_info import db_params
from lyric import lyric_search_and_input
from get_token import return_token
from typing import Dict, List, Union
from model.database import session_scope
from model.jun_model import *
from get_keyword import save_keyword_data
from user_data import user_data
from user_search_track import pick_data
from daily_search_ranking import daily_search_ranking
from search_spotify import *
from model.spotify_search import *


app = FastAPI()

class lyric_data(BaseModel):
    artist : str
    track : str
    track_id : int
    GENIUS_API_KEY : str = "U1RN70QWau9zk3qi3BPn_A-q4Bft_3jnw8uLBp2lVafQgOQiA_kjSEyxzr88eI9d"

class sp_data(BaseModel):
    artist : str
    album : str
    track : str

@app.get('/token/')
def update_token():
    access_token = return_token()
    return access_token

@app.post('/search/')
async def search_spotify(data:Spotify.SearchKeyword):
    access_token = update_token()
    search_header = {'Authorization': f'Bearer {access_token}'}

    parsed_data = Search.search_by_keywords(data.searchInput,limit=10)
    culled_data = Search.cull_data(parsed_data.tracks)
    
    search_data = Search.return_search(culled_data)
    return search_data

@app.post('/load/')
async def load_spotify(data:Spotify.SearchKeyword):
    access_token = update_token()
    search_header = {'Authorization': f'Bearer {access_token}'}

    parsed_data = Search.search_by_keywords(data.searchInput,limit=10)
    culled_data = Search.cull_data(parsed_data.tracks)
    Search.load_spotify(culled_data)

    album_ids = [album.id for album in culled_data.albums]
    for album_id in album_ids :
        Search.get_album_tracks(album_id)
    
    artist_ids = [artist.id for artist in culled_data.artists]
    for artist_id in artist_ids :
        Search.get_artist_albums(artist_id)

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
    
# @app.post("/sp_and_track_update/")
# def sp_track_input(item: sp_data):
#     artist = item.artist
#     album = item.album
#     track = item.track
#     d = get_sp_track_id(artist, album, track)
    
#     if d[0] is not None and d[1] is not None:  # get_sp_track_id 함수의 반환값이 None이 아닌지 확인
#         result = sp_and_track_input(d[0], d[1], artist, album, track)
#         return result
#     else:
#         raise HTTPException(status_code=404, detail="Track not found or error in processing.")